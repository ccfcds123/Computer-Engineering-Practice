# 导入XGO库和时间模块
from xgolib import XGO
import time
import math

class ComplexRobotDance:
    def __init__(self):
        """初始化机器狗舞蹈类"""
        self.dog = XGO("xgolite")
        self.dance_step = 0
        print("🎵 机器狗舞蹈机器人已初始化 🎵")
    
    def reset_to_stand(self):
        """复位到站立姿势"""
        print("复位到站立姿势...")
        self.dog.reset()
        time.sleep(1)
    
    def dance_intro(self):
        """开场动作 - 打招呼"""
        print("💃 开场：打招呼")
        
        # 前腿抬起打招呼
        self.dog.leg(1, [20, -15, 90])  # 左前腿抬起
        self.dog.leg(2, [20, -15, 90])  # 右前腿抬起
        time.sleep(1)
        
        # 左右摆动打招呼
        for i in range(3):
            self.dog.leg(1, [30, -20, 80])
            self.dog.leg(2, [10, -10, 100])
            time.sleep(0.3)
            self.dog.leg(1, [10, -10, 100])
            self.dog.leg(2, [30, -20, 80])
            time.sleep(0.3)
        
        self.reset_to_stand()
    
    def body_wave(self):
        """身体波浪动作"""
        print("🌊 身体波浪动作")
        
        # 身体前后平移波浪
        for i in range(4):
            # 前移并降低身体
            self.dog.translation('x', 30)
            self.dog.translation('z', -20)
            self.dog.attitude(['r', 'p', 'y'], [5, 10, 0])
            time.sleep(0.5)
            
            # 后移并抬高身体
            self.dog.translation('x', -30)
            self.dog.translation('z', 10)
            self.dog.attitude(['r', 'p', 'y'], [-5, -5, 0])
            time.sleep(0.5)
        
        self.reset_to_stand()
    
    def twist_dance(self):
        """扭腰舞 - 机身旋转配合腿部动作"""
        print("🔄 扭腰舞")
        
        # 设置迈步频率为快速
        self.dog.pace('fast')
        
        for i in range(6):
            # 左扭 + 抬左前腿
            self.dog.turn(30)
            self.dog.leg(1, [30, -25, 70])
            time.sleep(0.3)
            
            # 右扭 + 抬右前腿
            self.dog.turn(-30)
            self.dog.leg(1, [10, -15, 90])
            self.dog.leg(2, [30, -25, 70])
            time.sleep(0.3)
            
            # 中间复位
            self.dog.turn(0)
            self.dog.leg(2, [10, -15, 90])
            time.sleep(0.2)
        
        # 恢复默认迈步频率
        self.dog.pace('normal')
        self.reset_to_stand()
    
    def leg_sync_dance(self):
        """腿部同步舞蹈 - 对角线抬腿"""
        print("🦵 对角线同步舞蹈")
        
        for i in range(4):
            # 对角线1: 左前 + 右后
            self.dog.leg(1, [30, -30, 70])
            self.dog.leg(4, [30, 30, 70])
            time.sleep(0.4)
            
            # 复位
            self.dog.leg(1, [10, -15, 90])
            self.dog.leg(4, [10, 15, 90])
            time.sleep(0.2)
            
            # 对角线2: 右前 + 左后
            self.dog.leg(2, [30, -30, 70])
            self.dog.leg(3, [30, 30, 70])
            time.sleep(0.4)
            
            # 复位
            self.dog.leg(2, [10, -15, 90])
            self.dog.leg(3, [10, 15, 90])
            time.sleep(0.2)
    
    def spinning_top(self):
        """陀螺旋转 - 连续旋转"""
        print("🌀 陀螺旋转")
        
        # 快速连续旋转
        for i in range(4):
            self.dog.turn(180)
            time.sleep(1)
        
        # 反向旋转
        for i in range(4):
            self.dog.turn(-180)
            time.sleep(1)
        
        self.dog.turn(0)
        time.sleep(0.5)
    
    def periodic_shake(self):
        """周期性摇摆"""
        print("🎸 摇滚摇摆")
        
        # X轴周期运动 (前后)
        self.dog.periodic_tran('x', 1.5)  # 周期1.5秒
        time.sleep(3)
        self.dog.periodic_tran('x', 0)
        
        # Y轴周期运动 (左右)
        self.dog.periodic_tran('y', 1.2)  # 周期1.2秒
        time.sleep(2.4)
        self.dog.periodic_tran('y', 0)
        
        time.sleep(0.5)
    
    def march_forward_back(self):
        """行进舞步 - 前进后退组合"""
        print("🥾 行进舞步")
        
        # 设置步幅
        step_len = 40
        
        # 前进两步，后退两步的华尔兹节奏
        for i in range(2):
            # 前进
            self.dog.move('x', step_len)
            time.sleep(0.8)
            
            # 左转90度
            self.dog.turn(90)
            time.sleep(0.5)
            
            # 前进
            self.dog.move('x', step_len)
            time.sleep(0.8)
            
            # 右转90度回正
            self.dog.turn(-90)
            time.sleep(0.5)
        
        # 后退舞步
        for i in range(2):
            self.dog.move('x', -step_len)
            time.sleep(0.6)
            self.dog.move('x', -step_len)
            time.sleep(0.6)
        
        self.reset_to_stand()
    
    def altitude_variation(self):
        """高度变化舞步"""
        print("📈 高度变化")
        
        heights = [0, -20, -30, -20, 0, 20, 30, 20, 0]
        
        for h in heights:
            self.dog.translation('z', h)
            time.sleep(0.4)
        
        # 配合腿部动作
        for i in range(3):
            self.dog.translation('z', -25)
            self.dog.leg(2, [25, -25, 80])
            time.sleep(0.3)
            
            self.dog.translation('z', 15)
            self.dog.leg(2, [10, -15, 90])
            time.sleep(0.3)
        
        self.reset_to_stand()
    
    def attitude_dance(self):
        """姿态舞蹈 - 改变机身角度"""
        print("📐 姿态变化")
        
        # 姿态组合
        poses = [
            [0, 0, 0],      # 复位
            [10, 0, 0],     # 右滚转
            [-10, 0, 0],    # 左滚转
            [0, 15, 0],     # 俯仰
            [0, -15, 0],    # 仰头
            [0, 0, 30],     # 左偏航
            [0, 0, -30],    # 右偏航
            [5, 5, 15],     # 组合1
            [-5, -5, -15],  # 组合2
        ]
        
        for roll, pitch, yaw in poses:
            self.dog.attitude(['r', 'p', 'y'], [roll, pitch, yaw])
            time.sleep(0.8)
        
        self.reset_to_stand()
    
    def complex_sequence(self):
        """复杂动作序列 - 多动作组合"""
        print("✨ 复杂舞蹈序列")
        
        # 动作1: 抬起前腿 + 机身倾斜
        self.dog.leg(1, [35, -25, 70])
        self.dog.leg(2, [35, -25, 70])
        self.dog.attitude(['r', 'p', 'y'], [5, 10, 0])
        time.sleep(1)
        
        # 动作2: 保持前腿抬起，后腿弯曲
        self.dog.leg(3, [20, 30, 70])
        self.dog.leg(4, [20, 30, 70])
        self.dog.attitude(['r', 'p', 'y'], [-5, 5, 10])
        time.sleep(1)
        
        # 动作3: 前后交替
        for i in range(3):
            # 前腿弯曲
            self.dog.leg(1, [25, -30, 60])
            self.dog.leg(2, [25, -30, 60])
            time.sleep(0.3)
            
            # 后腿弯曲
            self.dog.leg(1, [10, -15, 90])
            self.dog.leg(2, [10, -15, 90])
            self.dog.leg(3, [25, 30, 60])
            self.dog.leg(4, [25, 30, 60])
            time.sleep(0.3)
        
        self.reset_to_stand()
    
    def finale_pose(self):
        """结束造型"""
        print("🌟 结束造型")
        
        # 优雅的结束动作
        self.dog.leg(1, [40, -30, 60])  # 左前腿高抬
        self.dog.leg(2, [20, -20, 80])  # 右前腿半抬
        self.dog.leg(3, [10, 15, 90])   # 左后腿正常
        self.dog.leg(4, [15, 25, 85])   # 右后腿微抬
        
        # 身体微倾
        self.dog.attitude(['r', 'p', 'y'], [5, 10, 5])
        time.sleep(2)
        
        # 鞠躬
        self.dog.attitude(['r', 'p', 'y'], [0, 30, 0])
        self.dog.leg(1, [20, -20, 80])
        self.dog.leg(2, [20, -20, 80])
        time.sleep(1.5)
        
        # 复位
        self.reset_to_stand()
        
        # 最后挥爪再见
        self.dog.leg(1, [30, -25, 70])
        time.sleep(1)
        self.dog.leg(1, [10, -15, 90])
        time.sleep(0.5)
        
        print("👋 舞蹈结束，谢谢观赏！")
    
    def perform_full_dance(self):
        """执行完整舞蹈序列"""
        print("\n" + "="*50)
        print("🎭 机器狗复杂舞蹈表演开始 🎭")
        print("="*50 + "\n")
        
        # 舞蹈序列
        self.dance_intro()          # 开场打招呼
        time.sleep(1)
        
        self.body_wave()            # 身体波浪
        time.sleep(1)
        
        self.twist_dance()          # 扭腰舞
        time.sleep(1)
        
        self.leg_sync_dance()       # 腿部同步舞蹈
        time.sleep(1)
        
        self.spinning_top()          # 陀螺旋转
        time.sleep(1)
        
        self.periodic_shake()        # 周期性摇摆
        time.sleep(1)
        
        self.march_forward_back()    # 行进舞步
        time.sleep(1)
        
        self.altitude_variation()    # 高度变化
        time.sleep(1)
        
        self.attitude_dance()        # 姿态舞蹈
        time.sleep(1)
        
        self.complex_sequence()      # 复杂序列
        time.sleep(1)
        
        self.finale_pose()           # 结束造型
        
        print("\n" + "="*50)
        print("✅ 全部舞蹈动作执行完成！")
        print("="*50)
    
    def cleanup(self):
        """清理资源"""
        print("清理资源...")
        self.dog.stop()
        print("已停止")


# 带机械臂的豪华版舞蹈
class RobotDanceWithArm(ComplexRobotDance):
    """带机械臂控制的豪华版舞蹈"""
    
    def __init__(self):
        super().__init__()
        print("🤖 机械臂版本初始化")
    
    def dance_with_arm(self):
        """机械臂配合舞蹈"""
        print("🎪 机械臂舞蹈表演")
        
        # 机械臂动作序列
        arm_positions = [
            (0, 0),      # 收回
            (50, 30),    # 前伸抬高
            (80, -20),   # 前伸降低
            (30, 60),    # 高抬
            (-30, 40),   # 后伸
            (0, 0),      # 收回
        ]
        
        # 夹爪动作
        claw_positions = [0, 128, 255, 128, 0]
        
        for i, (arm_x, arm_z) in enumerate(arm_positions):
            # 移动机械臂
            if -80 <= arm_x <= 155 and -95 <= arm_z <= 155:
                self.dog.arm(arm_x, arm_z)
            
            # 控制夹爪
            if i < len(claw_positions):
                self.dog.claw(claw_positions[i])
            
            # 配合身体动作
            self.dog.attitude(['r', 'p', 'y'], [5*i, 5*i, 0])
            time.sleep(1)
        
        # 复位机械臂
        self.dog.arm(0, 0)
        self.dog.claw(0)
        time.sleep(1)
    
    def perform_full_dance(self):
        """重写完整舞蹈序列，加入机械臂"""
        super().perform_full_dance()
        
        print("\n🎬 机械臂特别表演环节")
        self.dance_with_arm()
        print("机械臂表演结束\n")


# 主程序
if __name__ == "__main__":
    try:
        # 选择版本 (普通版或机械臂版)
        use_arm = True  # 如果有机械臂，改为 True
        
        if use_arm:
            dancer = RobotDanceWithArm()
        else:
            dancer = ComplexRobotDance()
        
        # 执行舞蹈
        dancer.perform_full_dance()
        
    except KeyboardInterrupt:
        print("\n⚠️ 舞蹈被中断")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        # 确保清理资源
        if 'dancer' in locals():
            dancer.cleanup()
    
    print("程序结束")