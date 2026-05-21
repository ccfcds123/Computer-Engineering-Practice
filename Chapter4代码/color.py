import cv2 as cv
import numpy as np
from camera import Dog_Camera
import time

class ColorRecognizer:
    # 预设常见颜色的HSV阈值（树莓派环境适配，可根据实际光线微调）
    COLOR_HSV_RANGES = {
        "red": [
            # 红色有两个HSV区间（Hue 0-10 和 170-180）
            (np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))
        ],
        "green": [
            (np.array([40, 70, 70]), np.array([70, 255, 255]))
        ],
        "blue": [
            (np.array([100, 120, 70]), np.array([130, 255, 255]))
        ]
    }

    def __init__(self, debug=False, target_colors=["red", "green", "blue"]):
        """
        初始化颜色识别器
        :param debug: 是否开启调试输出
        :param target_colors: 要识别的目标颜色列表（可选：red/green/blue）
        """
        self.debug = debug
        self.target_colors = target_colors
        # 初始化摄像头（复用Dog_Camera）
        self.camera = Dog_Camera(debug=debug)
        if not self.camera.isOpened():
            raise Exception("相机初始化失败，无法进行颜色识别")
        if self.debug:
            print("颜色识别器初始化完成")
            print(f"待识别颜色：{self.target_colors}")

    def _detect_color(self, frame):
        # 1. 转换为HSV色彩空间（去除RGB的亮度干扰）
        hsv_frame = cv.cvtColor(frame, cv.COLOR_RGB2HSV)
        # 2. 高斯模糊去噪（减少环境噪声干扰）
        hsv_frame = cv.GaussianBlur(hsv_frame, (5, 5), 0)

        detected_color = ""
        for color in self.target_colors:
            if color not in self.COLOR_HSV_RANGES:
                continue
            
            # 3. 遍历该颜色的HSV阈值区间，创建掩膜
            color_mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
            for (lower, upper) in self.COLOR_HSV_RANGES[color]:
                mask = cv.inRange(hsv_frame, lower, upper)
                color_mask = cv.bitwise_or(color_mask, mask)
            
            # 4. 形态学操作（去除小噪声）
            kernel = np.ones((5, 5), np.uint8)
            color_mask = cv.morphologyEx(color_mask, cv.MORPH_OPEN, kernel)
            color_mask = cv.morphologyEx(color_mask, cv.MORPH_DILATE, kernel)
            
            # 5. 检测轮廓（判断是否有目标颜色区域）
            contours, _ = cv.findContours(color_mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            if contours:
                # 过滤小轮廓（避免识别到微小噪声）
                valid_contours = [cnt for cnt in contours if cv.contourArea(cnt) > 500]
                if valid_contours:
                    detected_color = color
                    break  # 识别到第一个目标颜色即返回
        
        return detected_color

    def recognize_from_camera(self):
        try:
            print("开始实时颜色识别，按 Ctrl+C 退出...")
            last_color = ""  # 避免重复输出相同结果
            while True:
                # 获取当前帧
                success, frame = self.camera.get_frame()
                if not success:
                    print("获取图像失败，重试...")
                    time.sleep(0.5)
                    continue
                # 核心：检测颜色
                current_color = self._detect_color(frame)
                # 输出识别结果（仅当颜色变化时）
                if current_color and current_color != last_color:
                    print(f" 识别到颜色：{current_color}")
                    last_color = current_color
                elif not current_color:
                    last_color = ""  # 清空历史，便于重新识别
                time.sleep(0.1)  # 降低CPU占用
        except KeyboardInterrupt:
            print("\n 用户终止程序")
        except Exception as e:
            print(f" 识别过程出错: {str(e)}")
        finally:
            # 释放资源
            del self.camera
            if self.debug:
                print("颜色识别器已关闭")

if __name__ == '__main__':
    # 创建颜色识别器实例（开启调试，识别红/绿/蓝）
    # 若只需识别单一颜色，可修改target_colors，如 ["red"]
    recognizer = ColorRecognizer(debug=True, target_colors=["red", "green", "blue"])
    recognizer.recognize_from_camera()