# 导入XGO库
from xgolib import XGO
import time

class RobotDog:
    def __init__(self, model):
        self.dog = XGO(model)
    def translate(self, direction, distance):
        # 机身位置平移
        if direction == 'x':
            self.dog.translation('x', distance)
        elif direction == 'y':
            self.dog.translation('y', distance)
        # 等待移动完成
        time.sleep(0.5)
    def adjust_attitude(self, roll, pitch, yaw):
        # 机身姿态调整
        self.dog.attitude(['r', 'p', 'y'], [roll, pitch, yaw])
        # 等待姿态调整完成
        time.sleep(0.5)
    def periodic_motion(self, direction, period):
        # 机身周期运动
        if direction == 'x':
            self.dog.periodic_tran('x', period)
        elif direction == 'y':
            self.dog.periodic_tran('y', period)
        # 持续一定时间后停止
        time.sleep(period * 2)
        self.dog.periodic_tran(direction, 0)

    def dogstop(self):
        self.dog.stop()
   
# 创建XGO-LITE机器狗对象
my_dog = RobotDog("xgolite")

# 机身向前平移50mm
my_dog.translate('x', 50)
# 机身向右平移25mm
my_dog.translate('y', 25)
# 机身俯仰角设置为10°，偏航角设置为-4°，滚转角设置为8°
my_dog.adjust_attitude(8, 10, -4)

# 机身以3秒的周期，进行前后往复平移
my_dog.periodic_motion('x', 3)

my_dog.dogstop()


