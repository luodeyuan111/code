import airsim
import time
import math

# --- 必带：Tornado 补丁 (防止报错) ---
import tornado.iostream

if not hasattr(tornado.iostream, 'IOStream'):
    tornado.iostream.IOStream = tornado.iostream.BaseIOStream


# ------------------------------------

def main():
    print("=== 任务开始：连接模拟器 ===")
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)

    # 1. 解锁并起飞
    print("1. 正在起飞...")
    client.armDisarm(True)
    client.takeoffAsync().join()  # .join() 表示必须等起飞动作做完，程序才往下走

    # 2. 爬升到安全高度 (AirSim中，Z轴负数表示上方，-6 表示向上飞 6 米)
    print("2. 爬升至 6 米高度...")
    client.moveToZAsync(-6, 2).join()  # 速度 2m/s

    # -------------------------------------------------
    # 知识点：BodyFrame (机身坐标系)
    # vx: 正数向前，负数向后
    # vy: 正数向右，负数向左
    # vz: 正数向下，负数向上
    # -------------------------------------------------

    # 3. 向前飞 (vx=4 m/s, 持续 3秒)
    print("3. 全速前进 >>>")
    # 参数：vx, vy, vz, 持续时间, 驱动模式, 偏航模式
    client.moveByVelocityBodyFrameAsync(4, 0, 0, 3).join()
    time.sleep(0.5)  # 动作之间稍微停顿一下，更像真机

    # 4. 向右侧飞 (vy=4 m/s, 持续 3秒)
    print("4. 向右侧飞 >>>")
    client.moveByVelocityBodyFrameAsync(0, 4, 0, 3).join()
    time.sleep(0.5)

    # 5. 向后退 (vx=-4 m/s, 持续 3秒)
    print("5. 战术后撤 >>>")
    client.moveByVelocityBodyFrameAsync(-4, 0, 0, 3).join()
    time.sleep(0.5)

    # 6. 向左回正 (vy=-4 m/s, 持续 3秒)
    print("6. 向左归位 >>>")
    client.moveByVelocityBodyFrameAsync(0, -4, 0, 3).join()
    time.sleep(1)

    # 7. 原地旋转 360 度 (展示环绕视角)
    print("7. 开启上帝视角 (360度旋转)...")
    # rotateToYawAsync 指令是世界坐标系的角度
    # 我们先转到 90度，再180，再270，最后0度
    client.rotateToYawAsync(90).join()
    client.rotateToYawAsync(180).join()
    client.rotateToYawAsync(270).join()
    client.rotateToYawAsync(0).join()

    print("旋转完成！")

    # 8. 悬停一会儿
    print("8. 悬停保持...")
    client.moveByVelocityAsync(0, 0, 0, 3).join()  # 速度全为0即悬停

    # 9. 降落
    print("9. 任务完成，准备降落...")
    client.landAsync().join()

    # 锁定
    client.armDisarm(False)
    client.enableApiControl(False)
    print("=== 只有我看不到的降落，没有我飞不到的远方 ===")


if __name__ == "__main__":
    main()