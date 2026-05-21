import time
import sys
import os
from xgolib import XGO_DOG
# 尝试导入 xgolib_dog，假设它在当前目录
1
# ================= 动作数据定义 (移植自 C++) =================
# 模式定义
MODE_MOTOR = 0x01
MODE_BODY = 0x02
ACTIONS = {
        "Sit_Down": [
        {'duration': 3.0, 'mode': MODE_MOTOR, 'data': [50.1, 38.3, -0.1, 50.1, 38.3, -0.1, -30.8, 71.8, -0.1, -30.8, 71.8, -0.1, 0]},
    ]
}
class ActionExecutor:
    def __init__(self, dog):
        self.dog = dog
        # XGO 舵机编号列表，参考 xgolib_dog.py 中的 MOTOR_ID
        # 顺序通常是: 左前, 右前, 右后, 左后 (具体需参考 xgolib 中的定义顺序)
        # xgolib 定义: [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
        # 这对应4条腿，每条腿3个关节
        self.motor_ids = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
    def execute(self, action_name, postures):
        print(f"▶ 开始执行动作: {action_name}")
        
        for i, frame in enumerate(postures):
            mode = frame['mode']
            data = frame['data']
            duration = frame['duration']
            
            # print(f"  帧 {i+1}/{len(postures)}: 模式 {mode}, 耗时 {duration}s")
            if mode == MODE_MOTOR:
                # MODE_MOTOR: 直接控制 12 个舵机角度
                # C++ 数据是 12 个浮点数
                leg_angles = data[0:12]
                
                # 调用 xgolib 的 motor 函数
                # 注意: xgolib.motor(id_list, angle_list)
                self.dog.motor(self.motor_ids, leg_angles)
                # 检查是否有机械臂数据 (data[12] 是标志位)
                # 如果 data[12] == 0 且 data 长度足够，说明有机械臂控制
                if len(data) > 13 and data[12] == 0:
                    arm_angles = data[13:17]
                    # 假设机械臂 ID 为 51, 52, 53, 54 (xgolib 中有定义)
                    arm_ids = [51, 52, 53, 54]
                    self.dog.motor(arm_ids, arm_angles)
                
            elif mode == MODE_BODY:
                # MODE_BODY: 身体位姿控制
                # C++ data: [x, y, z, rol, pit, yaw, vx, vy, vyaw, ...]
                x, y, z = data[0], data[1], data[2]
                rol, pit, yaw = data[3], data[4], data[5]
                vx, vy, vyaw = data[6], data[7], data[8]
                
                # 1. 身体平移 (Translation)
                self.dog.translation(['x', 'y', 'z'], [x, y, z])
                
                # 2. 身体姿态 (Attitude)
                self.dog.attitude(['r', 'p', 'y'], [rol, pit, yaw])
                
                # 3. 移动速度
                if vx != 0: self.dog.move_x(vx)
                if vy != 0: self.dog.move_y(vy)
                if vyaw != 0: self.dog.turn(vyaw)
            # 等待动作执行
            time.sleep(duration)
            
        print(f"⏹ 动作 {action_name} 完成\n")
def main():
    # 1. 初始化机器狗
    # 端口号请根据实际情况修改: Windows通常是 'COMx', Linux/树莓派是 '/dev/ttyAMA0' 或 '/dev/ttyUSB0'
    port = "COM3"  # <--- 请在这里修改您的端口号
    
    print(f"正在连接机器狗 (端口: {port})...")
    try:
        # 实例化 XGO_DOG，它会自动读取固件版本并配置参数
        dog = XGO_DOG(port=port, verbose=False)
        print("✅ 连接成功! 固件版本:", dog.version)
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        print("请检查端口号是否正确，或 USB 线是否连接松动。")
        return
    # 2. 初始化执行器
    executor = ActionExecutor(dog)
    
    # 3. 菜单循环
    while True:
        print("-" * 30)
        print("机器狗动作控制器")
        print("1. 坐下 (Sit Down)")
        print("R. 复位 (Reset)")
        print("Q. 退出 (Quit)")
        print("-" * 30)
        
        choice = input("请输入选项: ").strip().upper()
        
        if choice == '1':
            executor.execute("Sit_Down", ACTIONS["Sit_Down"])
        elif choice == 'R':
            print("正在复位...")
            dog.reset()
        elif choice == 'Q':
            print("退出程序")
            break
        else:
            print("无效输入，请重试")
if __name__ == "__main__":
    main()