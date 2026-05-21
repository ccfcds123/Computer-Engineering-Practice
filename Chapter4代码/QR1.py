import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
from camera import Dog_Camera
import time

class QRCodeRecognizer:
    def __init__(self, debug=False):
        self.debug = debug
        self.camera = Dog_Camera(debug=debug)
        if not self.camera.isOpened():
            raise Exception("相机初始化失败，无法进行二维码识别")
        if self.debug:
            print("二维码识别器初始化完成")

    def recognize_from_camera(self):
        """从摄像头实时识别二维码（仅控制台输出）"""
        try:
            print("开始实时二维码识别，按 Ctrl+C 退出...")
            last_data = ""  # 避免重复输出相同结果
            while True:
                # 获取当前帧
                success, frame = self.camera.get_frame()
                if not success:
                    print("获取图像失败，重试...")
                    time.sleep(0.5)
                    continue

                # 转换为灰度图提高识别效率
                gray_frame = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)

                # 识别二维码
                qr_codes = decode(gray_frame)

                # 处理识别结果（仅输出新的二维码内容）
                current_data = ""
                for qr_code in qr_codes:
                    current_data = qr_code.data.decode('utf-8')
                    break  # 只取第一个识别到的二维码

                if current_data and current_data != last_data:
                    print(f" 识别到二维码：{current_data}")
                    last_data = current_data
                elif not current_data:
                    last_data = ""  # 清空历史，便于重新识别

                time.sleep(0.1)  # 降低CPU占用

        except KeyboardInterrupt:
            print("\n 用户终止程序")
        except Exception as e:
            print(f"识别过程出错: {str(e)}")
        finally:
            # 释放资源
            del self.camera
            if self.debug:
                print("二维码识别器已关闭")

if __name__ == '__main__':
    # 创建二维码识别器实例（开启调试模式）
    recognizer = QRCodeRecognizer(debug=True)
    recognizer.recognize_from_camera()