# 导入运动库
from xgolib import XGO

class RobotDogSensors:
    def __init__(self):
        self.dog = XGO("xgolite")

    def read_battery_level(self):
        """
        读取并返回机器狗的电量百分比。
        """
        battery_level = self.dog.read_battery()
        return battery_level

# 创建传感器对象
sensors = RobotDogSensors()
# 读取电量
battery_level = sensors.read_battery_level()
print(f"Current battery level: {battery_level}%")