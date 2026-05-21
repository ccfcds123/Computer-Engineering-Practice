# 机器狗方形路径行走+小球识别抓取主程序
from xgolib import XGO
import time
import threading
import socket
from dog_client import DogClient
import redball
from camera1 import get_global_camera  # 导入全局单例摄像头

def perform_recognition(recognize_duration=15, recognition_id=1, exit_on_error=False):
    """
    封装识别流程的函数（复用全局相机实例）
    :param recognize_duration: 识别持续时间
    :param recognition_id: 识别次数标识
    :param exit_on_error: 相机错误时是否退出程序
    """
    global global_client
    print(f"\n===== 开始第{recognition_id}次识别 =====")
    dog.stop()  # 识别期间确保机器狗静止
    time.sleep(0.5)
    
    try:
        # 检查全局客户端状态
        if global_client is None or not global_client.camera.isOpened():
            raise Exception("全局客户端/相机不可用")
        
        # 重启客户端运行状态
        global_client.running = True
        # 重新连接服务器
        if not global_client.connect():
            raise Exception("重新连接服务器失败")
        
        # 启动发送帧线程
        frame_thread = threading.Thread(target=global_client.send_frame, daemon=True)
        frame_thread.start()
        
        print(f"正在识别中，持续{recognize_duration}秒...")
        time.sleep(recognize_duration)
        
    except Exception as e:
        error_msg = f"⚠️ 第{recognition_id}次识别出错：{str(e)}"
        print(error_msg)
        if exit_on_error:
            print("由于错误，程序将退出")
            dog.reset()
            if global_client:
                global_client.stop()
            time.sleep(1)
            exit(1)
    finally:
        # 停止客户端（仅关闭socket）
        if global_client:
            global_client.running = False
            if global_client.client_socket:
                try:
                    global_client.client_socket.shutdown(socket.SHUT_RDWR)
                    global_client.client_socket.close()
                except:
                    pass
        print(f"===== 第{recognition_id}次识别完成 =====\n")
        time.sleep(0.5)

# 全局DogClient实例
global_client = None
angle = 35
angle_time = 3
x25 = 4.5
x40 = 2.67
x80 = 8
x110 = 7.5
x210 = 16.5
step = 15

def main():
    global global_client
    print("=== 机器狗方形路径行走程序开始 ===")
    
    # 1. 初始化机器狗
    global dog
    dog = XGO("xgomini")
    firmware = dog.read_firmware()
    if firmware == "Null":
        print("错误：无法连接到机器狗！")
        return
    print(f"成功连接到机器狗，固件版本：{firmware}")

    # 2. 初始化全局摄像头（整个程序仅这一次初始化）
    global_camera = get_global_camera(width=320, height=240, debug=True)
    if not global_camera.isOpened():
        print("错误：全局摄像头初始化失败！")
        dog.reset()
        return

    # 3. 初始化DogClient（复用全局摄像头）
    try:
        global_client = DogClient(
            host='172.18.17.47',
            port=5555,
            debug=True
        )
    except Exception as e:
        print(f"❌ DogClient初始化失败：{e}")
        dog.reset()
        global_camera.stop()
        return

#--------------------------------------------⬇⬇⬇代码编写区⬇⬇⬇-----------------------------------------------
    try:
        # ====================== 官方标准行走模块 ======================

        # 1. 前进 210cm = 2100mm
        print("第1段：向前走210cm...")
        dog.move('x', step)
        time.sleep(16.5)  # 等待走完
        dog.stop()
        time.sleep(0.5)

        # 2. 右转90°
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)

        # 3. 前进 40cm = 400mm
        print("第2段：向前走40cm")
        dog.move('x', step)
        time.sleep(x40)
        dog.stop()
        time.sleep(0.5)

        # 4. 第一个检查点
        print("第一个检查点")
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)
        time.sleep(1)
        print("左转90度")
        dog.turn(angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)

        # 5. 前进 80cm = 800mm
        print("第3段：向前走80cm")
        dog.move('x', step)
        time.sleep(x80)
        dog.stop()
        time.sleep(0.5)

        # 6. 第二个检查点
        print("第二个检查点")
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)
        time.sleep(1)
        print("左转90度")
        dog.turn(angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)

        # 7. 前进 40cm = 400mm
        print("第4段：向前走40cm")
        dog.move('x', step)
        time.sleep(x40)
        dog.stop()
        time.sleep(0.5)

        # 8. 右转90°
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)

        # 9. 前进 110cm = 1100mm
        print("第5段：向前走110cm")
        dog.move('x', step)
        time.sleep(x110)
        dog.stop()
        time.sleep(0.5)

        # 10. 右转90°
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)

        # 11. 前进 40cm = 400mm
        print("第6段：向前走40cm")
        dog.move('x', step)
        time.sleep(x40)
        dog.stop()
        time.sleep(0.5)

        # 12. 第三个检查点
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)
        time.sleep(1)
        print("左转90度")
        dog.turn(angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)

        # 13. 前进 80cm = 800mm
        print("第7段：向前走80cm")
        dog.move('x', step)
        time.sleep(x80)
        dog.stop()
        time.sleep(0.5)

        # 14. 第四个检查点
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)
        time.sleep(1)
        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)

        # 15. 前进 40cm = 400mm
        print("第8段：向前走40cm")
        dog.move('x', step)
        time.sleep(x40)
        dog.stop()
        time.sleep(0.5)

        print("右转90度")
        dog.turn(-angle)
        time.sleep(angle_time)
        dog.stop()
        time.sleep(0.5)
        time.sleep(1)

        print("🏁 方形路线完成！")

        # -------------------------- 识别模块 --------------------------
        dog.attitude('p', -12)
        perform_recognition(recognize_duration=15, recognition_id=1, exit_on_error=True)
        dog.attitude('p', 0)
        time.sleep(0.5)
        perform_recognition(recognize_duration=15, recognition_id=1, exit_on_error=True)
        time.sleep(0.5)

        # -------------------------- 小球抓取 --------------------------
        print("\n=====================================")
        print("======== 启动小球识别抓取程序 ========")
        print("=====================================")
        redball.redball_catch_main(dog)

        print("程序执行完成！")
#---------------------------------------------⬆⬆⬆代码编写区⬆⬆⬆------------------------------------

    except KeyboardInterrupt:
        print("程序被用户中断")
    finally:
        # 统一释放所有资源
        if global_client:
            global_client.stop()
        # 释放全局摄像头（核心：仅这里释放）
        global_camera.stop()
        # 重置机器狗
        print("重置机器狗...")
        dog.reset()
        time.sleep(1)

    print("=== 机器狗方形路径行走程序结束 ===")

if __name__ == "__main__":
    main()