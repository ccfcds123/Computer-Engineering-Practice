# camera.py 完整修改版
import cv2
import threading
from picamera2 import Picamera2

class SingletonDogCamera:
    """全局单例摄像头类（整个程序仅一个实例）"""
    # 类级别的实例和锁
    __instance = None
    __lock = threading.Lock()
    __camera_opened = False  # 标记摄像头是否已成功打开

    def __new__(cls, width=320, height=240, debug=False):
        """单例模式核心：确保仅创建一个实例"""
        with cls.__lock:
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
                # 初始化摄像头参数
                cls.__instance.width = width
                cls.__instance.height = height
                cls.__instance.debug = debug
                cls.__instance.picam2 = None
                # 初始化摄像头硬件
                cls.__instance._init_camera()
            return cls.__instance

    def _init_camera(self):
        """初始化摄像头（仅执行一次）"""
        if self.__camera_opened:
            if self.debug:
                print("✅ 摄像头已初始化，复用现有实例")
            return
        
        try:
            if self.debug:
                print("🔧 开始初始化全局摄像头...")
            # 清理残留的摄像头资源（避免之前的未释放问题）
            if self.picam2 is not None:
                self.picam2.stop()
                self.picam2.close()
            
            # 创建并配置摄像头
            self.picam2 = Picamera2()
            config = self.picam2.create_preview_configuration(
                main={"format": 'RGB888', "size": (self.width, self.height)}
            )
            self.picam2.configure(config)
            self.picam2.start()
            # 等待摄像头稳定
            import time
            time.sleep(0.5)
            
            # 验证摄像头是否可用
            test_frame = self.picam2.capture_array()
            if test_frame is None:
                raise RuntimeError("摄像头初始化后无法捕获测试帧")
            
            self.__class__.__camera_opened = True
            if self.debug:
                print("✅ 全局摄像头初始化成功！")
        except Exception as e:
            self.__class__.__camera_opened = False
            self.picam2 = None
            if self.debug:
                print(f"❌ 摄像头初始化失败：{e}")
            raise  # 抛出异常，让调用方感知

    def isOpened(self):
        """检查摄像头是否可用"""
        return self.__camera_opened and self.picam2 is not None

    def get_frame(self):
        """获取摄像头帧（统一接口）"""
        if not self.isOpened():
            if self.debug:
                print("⚠️ 摄像头未就绪，无法获取帧")
            return False, None
        
        try:
            frame = self.picam2.capture_array()
            return True, frame
        except Exception as e:
            if self.debug:
                print(f"⚠️ 获取摄像头帧失败：{e}")
            return False, None

    def stop(self):
        """释放摄像头资源（程序结束时调用）"""
        with self.__lock:
            if self.picam2 is not None:
                try:
                    self.picam2.stop()
                    self.picam2.close()
                    if self.debug:
                        print("✅ 摄像头资源已释放")
                except Exception as e:
                    if self.debug:
                        print(f"⚠️ 释放摄像头资源失败：{e}")
                finally:
                    self.picam2 = None
                    self.__class__.__camera_opened = False
                    self.__class__.__instance = None  # 重置单例

    def __del__(self):
        """析构函数：确保资源释放"""
        self.stop()

# 提供全局便捷获取函数（所有模块统一调用这个函数获取摄像头）
def get_global_camera(width=320, height=240, debug=False):
    """获取全局唯一的摄像头实例"""
    return SingletonDogCamera(width=width, height=height, debug=debug)