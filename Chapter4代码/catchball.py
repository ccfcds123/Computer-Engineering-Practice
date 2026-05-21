# XGO机器狗红色小球识别追踪抓取程序（复用全局摄像头版）
from xgolib import XGO
import time
import cv2
import numpy as np
from camera1 import get_global_camera  # 导入全局单例摄像头

# 让机器狗趴下的函数（最大程度降低）
def make_dog_lie_down(dog):
    """让机器狗趴下，最大程度降低高度"""
    dog.translation('z', 75)  # 最低身高
    dog.attitude('p', 35)     # 最大幅度低头
    time.sleep(1.5)
    print("机器狗已趴下，准备寻找小球...")

# 机械臂精准抓取函数（关键：抓取时末端必须足够低）
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
    dog.claw(200)
    time.sleep(2)
    
    dog.arm(60, 80)    # 完全抬起到安全高度
    time.sleep(1.2)
    
    # 调整身体姿态展示
    dog.attitude('p', 10)
    time.sleep(1)

# 识别红色小球的函数
def detect_red_ball_on_table(image):
    """
    专门针对桌面小球的识别函数
    返回: (x, y, radius) 或 (0, 0, 0) 如果未检测到
    """
    # 转换到HSV色彩空间
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # 针对桌面环境优化的红色HSV范围
    lower_red1 = np.array([0, 120, 60])
    upper_red1 = np.array([15, 255, 255])
    lower_red2 = np.array([160, 120, 60])
    upper_red2 = np.array([180, 255, 255])
    
    # 创建掩码
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)
    
    # 形态学操作去除噪声
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 应用掩码
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    
    # 转换为灰度图
    gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    
    # 使用高斯模糊减少噪声
    gray = cv2.GaussianBlur(gray, (7, 7), 2)
    
    # 使用霍夫圆变换检测圆形
    circles = cv2.HoughCircles(
        gray, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=25,
        param1=40,
        param2=18,
        minRadius=10,
        maxRadius=80
    )
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        # 找到最大的圆
        max_circle = max(circles, key=lambda c: c[2])
        return int(max_circle[0]), int(max_circle[1]), int(max_circle[2])
    
    return 0, 0, 0

# 根据距离计算实际距离的函数
def calculate_distance_from_lie_position(radius):
    """
    从趴着位置根据半径估算距离（cm）
    """
    if radius == 0:
        return float('inf')
    
    k = 600
    distance_cm = k / radius
    return distance_cm

# 核心：小球识别抓取主函数（对外暴露的调用入口）
def redball_catch_main(dog):
    """
    小球识别抓取主流程（接收已初始化的机器狗实例）
    """
    print("\n=== 开始执行红色小球识别追踪抓取任务 ===")
    
    # 核心修改：获取全局摄像头实例（不再单独初始化）
    cam = get_global_camera(debug=True)
    if not cam.isOpened():
        print("❌ 全局摄像头未就绪，无法执行抓取任务")
        return

    # 第一步：让机器狗趴下
    make_dog_lie_down(dog)

    # 第二步：搜索和抓取小球
    print("开始寻找红色小球...")
    search_attempts = 0
    max_attempts = 25

    while search_attempts < max_attempts:
        # 使用全局摄像头获取帧
        success, frame = cam.get_frame()
        if not success:
            print(f"第{search_attempts + 1}次尝试：获取图像失败")
            search_attempts += 1
            time.sleep(0.6)
            continue
        
        # 识别桌面小球
        x, y, radius = detect_red_ball_on_table(frame)
        
        if radius > 0:
            # 计算距离
            distance = calculate_distance_from_lie_position(radius)
            print(f"发现红色小球！位置: ({x}, {y}), 半径: {radius}px, 距离: {distance:.1f}cm")
            
            # 在图像上绘制检测结果（可选）
            cv2.circle(frame, (x, y), radius, (0, 255, 0), 2)
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)
            
            # 根据距离判断行动
            if distance > 18.0:
                print(f"小球太远了({distance:.1f}cm)，向前移动...")
                dog.move_x(2)
                time.sleep(1.0)
                dog.stop()
                time.sleep(0.5)
                
            elif distance < 12.0:
                print(f"小球太近了({distance:.1f}cm)，向后移动...")
                dog.move_x(-3)
                time.sleep(0.8)
                dog.stop()
                time.sleep(0.5)

            elif 12.0 <= distance <= 18.0:
                print(f"距离合适({distance:.1f}cm)，准备抓取！")
                
                # 调整左右位置（更精确居中）
                center_x = 160
                if abs(x - center_x) > 12:
                    if x < center_x:
                        print("小球偏左，向左移动...")
                        dog.move_y(2)
                    else:
                        print("小球偏右，向右移动...")
                        dog.move_y(-2)
                    time.sleep(0.6)
                    dog.stop()
                    time.sleep(0.5)
                    continue
                
                # 执行精准抓取
                catch_arm_from_lie_position(dog)
                print("红色小球抓取完成！")
                break
                
        else:
            print(f"第{search_attempts + 1}次尝试：未检测到红色小球")
            if search_attempts % 4 == 3:
                print("轻微转圈搜索小球...")
                dog.turn(45)
                time.sleep(0.6)
                dog.stop()
                time.sleep(0.5)
        
        search_attempts += 1
        time.sleep(0.6)

    # 第三步：任务完成，让机器狗站起来
    print("小球抓取任务完成，让机器狗站起来...")
    dog.action(2)
    time.sleep(3)
    
    print("=== 红色小球识别追踪抓取任务结束 ===")

# 释放摄像头资源（实际调用全局释放）
def release_redball_camera():
    """释放小球识别摄像头（统一调用全局摄像头释放）"""
    cam = get_global_camera()
    cam.stop()
    print("✅ 全局摄像头已释放（小球识别模块）")

# 独立运行测试（可选）
if __name__ == "__main__":
    # 初始化XGO机器狗
    dog = XGO(port="/dev/ttyAMA0", version="xgolite")
    firmware = dog.read_firmware()
    if firmware == "Null":
        print("错误：无法连接到机器狗！")
        exit()
    else:
        print(f"成功连接到机器狗，固件版本：{firmware}")
    
    # 执行抓取流程
    redball_catch_main(dog)
    
    # 程序结束，重置机器狗
    print("程序结束，重置机器狗...")
    dog.reset()
    release_redball_camera()
    print("=== XGO机器狗红色小球识别追踪抓取程序结束 ===")