# 导入运动库
from xgolib import XGO
import time

class RobotDogArm:
    def __init__(self):
        self.dog = XGO("xgolite")

    def dogstop(self):
        self.dog.stop()

    def dogreset(self):
        self.dog.reset()

    def move_arm(self, arm_x, arm_z):
        """
        控制机械臂移动到指定位置。
        
        :param arm_x: 水平面移动距离(mm)
        :param arm_z: 垂直面移动距离(mm)
        """
        # 检查输入值是否在机械臂工作范围内
        if -80 <= arm_x <= 155 and -95 <= arm_z <= 155:
            self.dog.arm(arm_x, arm_z)
        else:
            print("Error: Arm position out of range.")

    def control_claw(self, pos):
        """
        控制机械臂夹爪的开合。
        
        :param pos: 夹爪开合位置(0-255)
        """
        self.dog.claw(pos)

# 创建机器狗机械臂对象
my_arm = RobotDogArm()

# 移动机械臂到指定位置
my_arm.move_arm(20, 30)  # 例如：向前移动20mm，向上移动30mm

time.sleep(2)

# 控制夹爪开合
my_arm.control_claw(128)  # 例如：夹爪开合至中间位置
time.sleep(2)

# 夹爪完全张开
my_arm.control_claw(0)
time.sleep(2)

# 夹爪完全闭合
my_arm.control_claw(255)
time.sleep(2)

my_arm.dogreset()
my_arm.dogstop()