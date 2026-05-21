import time
from xgolib import XGO_DOG

PORT = "COM3"  # 请修改为您的实际端口

# ================= 常量定义 =================
MODE_MOTOR = 0x01
MODE_BODY = 0x02

# ================= 全舵机动作定义 =================
# 每个data数组包含 15 个舵机角度:
# [腿部12个(11,12,13...43), 机械臂3个(51,52,53)]
# 机械臂角度假设: [Arm1, Arm2, Claw]
FULL_MOTOR_ACTION = [
    # 帧1: 初始站立 + 机械臂收回
    {'duration': 10.0, 'mode': MODE_MOTOR, 'data': [
        # 腿部12个 (标准站立) ，机械臂3个
        # 0, 56, -20,   0, 56, 0,   0, 56, 0,   0, 56, 0,  30, 30, -50
        50.1, 38.3, -0.1, 50.1, 38.3, -0.1, -30.8, 71.8, -0.1, -30.8, 71.8, -0.1, 0
    ]
        
    },
    
    
]

def run_action(dog, action_list):
    """
    解析并执行动作列表 (支持全舵机控制)
    """
    print(f"▶ 开始执行动作 (共 {len(action_list)} 帧)...")
    
    # 腿部舵机 ID (12个)
    leg_ids = [11, 12, 13, 21, 22, 23, 31, 32, 33, 41, 42, 43]
    # 机械臂舵机 ID (3个: 51=根部, 52=中间, 53=夹爪)
    # 具体ID需根据xgolib或文档确认，通常是 51,52,53 或 51,52,53,54
    arm_ids = [51, 52, 53] 

    for i, frame in enumerate(action_list):
        mode = frame['mode']
        data = frame['data']
        duration = frame['duration']
        
        print(f"\r  执行第 {i+1} 帧...", end="")

        if mode == MODE_MOTOR:
            # --- 关节控制模式 ---
            
            # 1. 控制腿部 (前12个数据)
            if len(data) >= 12:
                leg_angles = data[0:12]
                dog.motor(leg_ids, leg_angles)
            
            # 2. 控制机械臂 (第13个及以后)
            if len(data) > 12:
                # 提取机械臂数据
                # 假设 data[12] 是 Arm1, data[13] 是 Arm2, data[14] 是 Claw
                arm_angles = data[12:]
                
                # 如果数据不够3个，只取有的部分
                current_arm_ids = arm_ids[:len(arm_angles)]
                
                # 调用 motor 控制机械臂
                # 注意: 夹爪(53) 有时需要用专门的 claw 函数，这里尝试直接用 motor
                dog.motor(current_arm_ids, arm_angles)

        elif mode == MODE_BODY:
            # --- 身体控制模式 ---
            # 1. 基础位姿 (前6个)
            if len(data) >= 6:
                x, y, z = data[0], data[1], data[2]
                r, p, yw = data[3], data[4], data[5]
                dog.translation(['x', 'y', 'z'], [x, y, z])
                dog.attitude(['r', 'p', 'y'], [r, p, yw])
            
        time.sleep(duration)
    
    print("\n✅ 动作执行完毕")

def main():
    print(f"正在连接机器狗 (端口: {PORT})...")
    try:
        dog = XGO_DOG(port=PORT, verbose=False, version="xgolite")
        print(f"连接成功! 固件版本: {dog.version}")
        
        print("复位...")
        dog.reset()
        time.sleep(1)
        
        run_action(dog, FULL_MOTOR_ACTION)
        
        time.sleep(1)
        print("复位...")
        dog.reset()
        
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
