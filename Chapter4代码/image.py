from email.mime import image

from picamera2 import Picamera2
import time
import cv2 as cv
import numpy as np
import os  # 导入os模块用于路径处理和创建目录

class Dog_Camera(object):
    def __init__(self, width=640, height=480, debug=False):
        self.__debug = debug
        self.__state = False
        self.__width = width
        self.__height = height
        # 定义照片保存路径
        self.save_path = "/home/pi/Pictures"
        # 确保保存目录存在，不存在则创建
        os.makedirs(self.save_path, exist_ok=True)
        print("---------Camera Init...------------")

        self.__picam2 = Picamera2()
        config = self.__picam2.create_preview_configuration(main={"format": 'RGB888', "size": (self.__width, self.__height)})
        self.__picam2.configure(config)
        self.__picam2.start()
        
        self.__state = True
        
        if self.__debug:
            print("---------Camera Init OK!------------")

    def __del__(self):
        if self.__debug:
            print("---------Del Camera!------------")
        self.__picam2.stop()
        self.__state = False

    def isOpened(self):
        return self.__state

    def get_frame(self):
        if self.__state:
            frame = self.__picam2.capture_array()
            return True, frame
        else:
            return False, None

    def get_frame_jpg(self, text="", color=(0, 255, 0)):
        success, image = self.get_frame()
        if not success:
            return success, bytes({1})

        if text != "":
            cv.putText(image, str(text), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        success, jpeg = cv.imencode('.jpg', image)
        return success, jpeg.tobytes()

    def take_photo(self):
        """拍照并保存至/home/pi/Pictures路径"""
        if not self.__state:
            print("相机未开启，无法拍照")
            return False
        
        # 获取当前帧
        success, frame = self.get_frame()
        if not success:
            print("获取图像失败，无法拍照")
            return False
        
        # 生成带时间戳的文件名，避免重复
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"photo_{timestamp}.jpg"
        # 拼接完整保存路径
        full_path = os.path.join(self.save_path, filename)
        full_path_gray = os.path.join(self.save_path, f"photo_{timestamp}_gray.jpg")
        full_path_hsv = os.path.join(self.save_path, f"photo_{timestamp}_hsv.jpg")
        full_path_h_channel = os.path.join(self.save_path, f"photo_{timestamp}_h_channel.jpg")
        full_path_otsu = os.path.join(self.save_path, f"photo_{timestamp}_otsu.jpg")

        
        # 转换颜色空间：RGB转BGR（OpenCV保存图像默认用BGR格式）
        frame_bgr = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        frame_rgb = cv.cvtColor(frame_bgr, cv.COLOR_BGR2RGB)
        frame_gray = cv.cvtColor(frame_bgr, cv.COLOR_BGR2GRAY)
        hsv = cv.cvtColor(frame_bgr, cv.COLOR_BGR2HSV)
        h_channel = hsv[:,:,0]
        (thresh, im_bw) = cv.threshold(hsv[:,:,0], 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        

        # 保存图片
        cv.imwrite(full_path, frame)
        cv.imwrite(full_path_gray, frame_gray)
        cv.imwrite(full_path_hsv, hsv)
        cv.imwrite(full_path_h_channel, h_channel)
        cv.imwrite(full_path_otsu, im_bw)
        
        if self.__debug:
            print(f"照片已保存至: {full_path}")
        return True

if __name__ == '__main__':
    # 创建相机实例（开启调试模式）
    camera = Dog_Camera(debug=True)
    # 程序运行后直接拍一张照片
    camera.take_photo()
    # 释放相机资源
    del camera
    # 关闭所有可能的窗口
    cv.destroyAllWindows()