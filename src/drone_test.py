
# main.py
import cv2
import time
import sys
import airsim
import numpy as np  # 导入 numpy
import os
import msvcrt

sys.path.append('./utils')
from Drone_Interface.rgb_data_extractor import RGBDataExtractor
from Drone_Interface.rgb_data_extractor import FrameBuffer

def main():
    # 初始化
    extractor = RGBDataExtractor(drone_name="Drone1", save_images=False)
    camera_name = "front_camera"  # 指定摄像头名称
    display_frame = None  # 用于存储要显示的帧
    client = extractor.client  # 获取 airsim client

    # 初始化帧缓冲区
    frame_buffer = FrameBuffer()

    # 创建显示窗口（非阻塞），避免 GUI 无响应
    cv2.namedWindow("Drone View", cv2.WINDOW_NORMAL)

    # 移动速度
    move_speed = 10  # 单位：米/秒

    try:
        print("开始视频流捕获...\n键盘输入决定行为 :\n'e'键保存当前帧\n'q'键退出\n'w'前进\n's'后退\n'a'左移\n'd'右移\n','上升\n'.'下降\n")
        while True:
            if msvcrt.kbhit():  # 检查是否有按键被按下
                key = ord(msvcrt.getch())  # 读取按键的 ASCII 码
                print(f"按下的键的 ASCII 码 (msvcrt): {key}, 字符: {chr(key)}")
                # 控制无人机移动
                if key == ord('w'):
                    client.moveByVelocityBodyFrameAsync(move_speed, 0, 0, 0.5)  # 前进
                elif key == ord('s'):
                    client.moveByVelocityBodyFrameAsync(-move_speed, 0, 0, 0.5)  # 后退
                elif key == ord('a'):
                    client.moveByVelocityBodyFrameAsync(0, -move_speed, 0, 0.5)  # 左
                elif key == ord('d'):
                    client.moveByVelocityBodyFrameAsync(0, move_speed, 0, 0.5)  # 右
                elif key == ord(','):
                    client.moveByVelocityBodyFrameAsync(0, 0, -move_speed, 0.5)  # 上
                elif key == ord('.'):
                    client.moveByVelocityBodyFrameAsync(0, 0, move_speed, 0.5)  # 下
                elif key == ord('e'):
                    timestamp = int(time.time() * 1000)
                    rgb_data = extractor.capture_rgb_images(timestamp)
                    if camera_name in rgb_data:
                        frame = rgb_data[camera_name]

                        # 检查帧是否为空或无效
                        if frame is not None and isinstance(frame, np.ndarray) and frame.size > 0:
                            # 更新帧缓冲区
                            frame_buffer.update(frame)
                            frame_t, frame_t_plus_1 = frame_buffer.get_frames()

                            # 现在你可以访问 frame_t (前一帧) 和 frame_t_plus_1 (当前帧)
                            if frame_t is not None:
                                #print("前一帧已获得")
                                pass
                            else:
                                pass
                                #print("还未获得前一帧")
                            if frame_t_plus_1 is not None:
                                #print("获得当前帧")
                                pass
                            else:
                                pass
                                #print("未获得当前帧")
                            display_frame = frame  #为了展示当前图像，所以还是把当前帧给display——frame进行展示
                            print(f"已捕获相机{camera_name}的当前帧（时间戳：{timestamp}）")
                        else:
                            print(f"警告：从相机 {camera_name} 获取的帧为空或无效")
                    else:
                        print(f"警告：无法获取相机 {camera_name} 的图像")
                elif key == ord('q'):
                    print("退出程序。")
                    break
                else:
                    print("无效键，请使用指定的键进行操作。")
            else:
                time.sleep(0.01)  # 暂停 10 毫秒

            # 显示图像（如果已捕获）
            if display_frame is not None:
                try:
                    # AirSim 返回的是 RGB，OpenCV 使用 BGR，用于正确显示颜色
                    if isinstance(display_frame, np.ndarray) and display_frame.ndim == 3 and display_frame.shape[2] == 3:
                        show_frame = cv2.cvtColor(display_frame, cv2.COLOR_RGB2BGR)
                    else:
                        show_frame = display_frame
                    cv2.imshow("Drone View", show_frame)
                except Exception as e:
                    print(f"显示图像时出错: {e}")

            # 处理 GUI 事件，防止窗口变为未响应
            cv2.waitKey(1)

            # 得到RGB图像数据———— frame_buffer中的frame_t和frame_t_plus_1
            frame_t, frame_t_plus_1 = frame_buffer.get_frames()
            # 你可以在这里对 frame_t 和 frame_t_plus_1 进行处理,用Visual_process里面的函数进行处理
    except Exception as e:
        print(f"发生错误: {e}")

    finally:
        extractor.disconnect()
        try:
            cv2.destroyAllWindows()
        except:
            pass

if __name__ == "__main__":
    main()


