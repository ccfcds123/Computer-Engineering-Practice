from picamera2 import Picamera2
import time
import cv2 as cv
import numpy as np
import os
from datetime import datetime
from xgolib import XGO
dog = XGO("xgomini")
dog.attitude('p', -12)  
class Dog_Camera(object):
    """狗狗相机类 - 自动录制10秒后退出"""
    def __init__(self, width=640, height=480, debug=False):
        self.__debug = debug
        self.__state = False
        self.__width = width
        self.__height = height
        
        # 新增录制相关属性
        self.__is_recording = False
        self.__video_writer = None
        self.__video_path = "/home/pi/xgoVideos/"
        self.__record_start_time = 0  # 录制开始时间
        self.__record_duration = 60    # 固定录制时长

        print("---------Camera Init...------------")
        # 初始化相机
        self.__picam2 = Picamera2()
        config = self.__picam2.create_preview_configuration(main={"format": 'RGB888', "size": (self.__width, self.__height)})
        self.__picam2.configure(config)
        self.__picam2.start()
        self.__state = True
        
        # 自动创建视频保存目录
        if not os.path.exists(self.__video_path):
            os.makedirs(self.__video_path)
            if self.__debug:
                print(f"---------创建视频目录: {self.__video_path}------------")
        
        if self.__debug:
            print("---------Camera Init OK!------------")

    def __del__(self):
        """析构函数：释放所有资源"""
        if self.__debug:
            print("---------Del Camera!------------")
        self.stop_recording()
        self.__picam2.stop()
        self.__state = False

    def isOpened(self):
        """判断相机是否开启"""
        return self.__state

    def get_frame(self):
        """获取图像帧，并在录制时写入视频"""
        if self.__state:
            frame = self.__picam2.capture_array()
            # 录制中则写入帧
            if self.__is_recording and self.__video_writer is not None:
                self.__video_writer.write(frame)
            return True, frame
        else:
            return False, None

    def get_frame_jpg(self, text="", color=(0, 255, 0)):
        """获取带文字标注的JPG格式图像"""
        success, image = self.get_frame()
        if not success:
            return success, bytes({1})

        if text != "":
            cv.putText(image, str(text), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        success, jpeg = cv.imencode('.jpg', image)
        return success, jpeg.tobytes()

    def start_recording(self):
        """开始10秒自动录制"""
        if not self.__state:
            if self.__debug:
                print("---------相机未开启，无法录制------------")
            return False
        
        if self.__is_recording:
            if self.__debug:
                print("---------已在录制中------------")
            return False
        
        # 生成时间戳文件名（避免重复）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"{self.__video_path}dog_video_{timestamp}.avi"
        
        # 配置视频写入器（MJPG编码，兼容树莓派）
        fourcc = cv.VideoWriter_fourcc(*'MJPG')
        fps = 30  # 帧率（可根据摄像头性能调整为15/20）
        self.__video_writer = cv.VideoWriter(video_filename, fourcc, fps, (self.__width, self.__height))
        
        if self.__video_writer.isOpened():
            self.__is_recording = True
            self.__record_start_time = time.time()  # 记录录制开始时间
            if self.__debug:
                print(f"---------开始10秒录制: {video_filename}------------")
            return True
        else:
            if self.__debug:
                print("---------视频写入器初始化失败------------")
            self.__video_writer = None
            return False

    def stop_recording(self):
        """停止录制并释放视频写入器"""
        if not self.__is_recording:
            return True
        
        self.__is_recording = False
        if self.__video_writer is not None:
            self.__video_writer.release()
            self.__video_writer = None
            if self.__debug:
                print("---------10秒录制完成，视频已保存------------")
        return True

    def is_record_finished(self):
        """检查10秒录制是否完成"""
        if not self.__is_recording:
            return False
        elapsed_time = time.time() - self.__record_start_time
        return elapsed_time >= self.__record_duration  # 超过10秒返回True

if __name__ == '__main__':
    # 初始化相机（开启调试模式，可改为False关闭日志）
    camera = Dog_Camera(debug=True)
    
    # 程序启动后自动开始10秒录制
    camera.start_recording()
    
    average = False
    m_fps = 0
    t_start = time.time()
    
    # 主循环：显示画面 + 等待录制完成
    while camera.isOpened():
        # FPS计算（保留原逻辑）
        if average:
            ret, frame = camera.get_frame()
            m_fps += 1
            fps = m_fps / (time.time() - t_start)
        else:
            start = time.time()
            ret, frame = camera.get_frame()
            end = time.time()
            fps = 1 / (end - start)
        
        # 绘制FPS和录制状态/剩余时间
        fps_text = f"FPS: {int(fps)}"
        cv.putText(frame, fps_text, (20, 30), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 200, 0), 1)
        
        # 计算剩余录制时间
        if camera.is_record_finished():
            record_text = "录制完成！即将退出..."
            record_color = (0, 255, 255)  # 黄色
        else:
            elapsed = time.time() - camera._Dog_Camera__record_start_time
            remaining = round(camera._Dog_Camera__record_duration - elapsed, 1)
            record_text = f"自动录制中 | 剩余: {remaining}s"
            record_color = (0, 0, 255)  # 红色
        
        cv.putText(frame, record_text, (20, 60), cv.FONT_HERSHEY_SIMPLEX, 0.7, record_color, 2)
        
        cv.imshow('Auto Record 10s', frame)

        # 检查录制是否完成，完成则退出循环
        if camera.is_record_finished():
            camera.stop_recording()
            # 延迟0.5秒让用户看到"录制完成"提示，再退出
            time.sleep(0.5)
            break
        
        # 备用退出（按q/ESC可强制退出）
        k = cv.waitKey(1) & 0xFF
        if k == 27 or k == ord('q'):
            camera.stop_recording()
            break
    
    # 释放所有资源并退出程序
    del camera
    cv.destroyAllWindows()
    print("---------程序已退出------------")