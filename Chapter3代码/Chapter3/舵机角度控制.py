from xgolib import XGO
import time

class RobotDogSensors:
    def __init__(self):
        self.dog = XGO("xgolite")

    def read_servo_angles(self):
        """
        读取并返回所有舵机的角度列表。
        """
        servo_angles = self.dog.read_motor()
        return servo_angles
    
    def control_servo_angles(self,motor_id,data):
        self.dog.motor(motor_id, data)
    
    def servo_reset(self):
        self.dog.reset()

# 创建传感器对象
sensors = RobotDogSensors()

# 读取舵机角度
servo_angles = sensors.read_servo_angles()
print(f"Servo angles: {servo_angles}")

sensors.control_servo_angles(11,10)
time.sleep(2)

sensors.servo_reset()


