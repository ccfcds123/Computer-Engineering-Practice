from xgolib import XGO
import time
import cv2
import numpy as np

def catch_arm_from_lie_position(dog):
    """从趴着位置精准抓取小球 - 确保抓取瞬间末端高度足够低"""
    print("执行精准抓取动作...")

    # 保持最低姿态
    dog.translation('z', 75)
    dog.attitude('p', 30)
    
    # 关闭稳定模式
    dog.arm_mode(0)
    time.sleep(0.3)
    
    # 打开夹爪
    dog.claw(0)
    time.sleep(0.4)
    
    # 直接移动到抓取位置（关键：z坐标设为-95，这是机械臂的最低极限）
    dog.arm(120, -5)
    dog.claw(0)    
    time.sleep(2.0)    # 给足时间到达最低位置

    # 下降机械臂（缓慢安全下降）
    dog.arm(120, -25)  
    time.sleep(1.0)
    
    # 立即闭合夹爪抓取（在最低位置抓取）
    dog.claw(0)
    time.sleep(2)
    dog.claw(200)
    time.sleep(2)
    
    dog.arm(60, 80)    # 完全抬起到安全高度
    time.sleep(1.2)
    
    # 调整身体姿态展示
    dog.attitude('p', 10)
    time.sleep(1)


if __name__ == '__main__':
    dog = XGO(port="/dev/ttyAMA0", version="xgolite")
    
    catch_arm_from_lie_position(dog)