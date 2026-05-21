from xgolib import XGO
import time

dog = XGO("xgolite")
targets = [120, 60, 0]
speed = 30
threshold = 5

for target in targets:
    print(f"目标: {target}°")
    while True:
        time.sleep(0.1)
        current = dog.read_yaw()
        if current == 0: continue
        error = target - current
        # 角度环绕处理
        if error > 180: error -= 360
        if error < -180: error += 360
        if abs(error) <= threshold:  # 到达
            dog.stop()
            time.sleep(2)
            break
        elif error > 0:  # 左转
            dog.turn(speed)
        else:  # 右转
            dog.turn(-speed)

dog.stop()