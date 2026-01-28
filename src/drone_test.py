import airsim
import numpy as np
import cv2
import os
import time

import sys
sys.path.append('../')  # 将项目根目录添加到搜索路径

from Drone_Interface.rgb_data_extractor_utf8 import RGBDataExtractor



def main():
    # 初始化RGB数据提取器（无人机名称为Drone1），不将每帧保存到磁盘
    extractor = RGBDataExtractor(drone_name="Drone1", save_images=False)

    target_fps = 10  # 目标帧率（可根据需要调整）
    interval = 1.0 / target_fps

    try:
        print(f"开始连续捕获（按 'q' 退出），目标帧率：{target_fps} FPS")
        while True:
            start = time.time()
            timestamp = int(start * 1000)

            rgb_data = extractor.capture_rgb_images(timestamp)

            # 实时显示每个相机的图像
            for cam_name, img in rgb_data.items():
                # extractor 返回的是 RGB 格式，显示前转换为 BGR
                try:
                    disp = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                except Exception:
                    disp = img
                cv2.imshow(f"Camera: {cam_name}", disp)

            # 键盘事件处理：按 'q' 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print('检测到退出键，停止采集')
                break

            # 控制帧率
            elapsed = time.time() - start
            to_sleep = interval - elapsed
            if to_sleep > 0:
                time.sleep(to_sleep)

    finally:
        extractor.disconnect()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
