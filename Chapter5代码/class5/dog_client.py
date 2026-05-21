import socket
import threading
import time
import struct
import json
import cv2  # 新增cv2导入
from yuyin import play_speech_directly
import asyncio
from camera1 import get_global_camera  # 导入全局单例摄像头

CLASS_NAMES = ["low", "normal", "higher","three","six","No helmet","helmet","B","D","A","C"]
CLASS_CN_MAP = [
    "偏低为异常状态", "正常为正常状态", "较高为异常状态", "35212偏高变压器过压", "10561偏低变压器欠压",
    "未佩戴安全帽", "佩戴安全帽", "B区域", "D区域", "A区域", "C区域"
]


class DogClient:
    def __init__(self, host='172.18.17.47', port=5555, debug=False, timeout=10):
        self.host = host
        self.port = port
        self.debug = debug
        self.timeout = timeout
        self.running = False
        self.client_socket = None
        self.lock = threading.Lock()
        
        # 核心修改：使用全局摄像头实例
        self.camera = get_global_camera(width=320, height=240, debug=debug)
        if not self.camera.isOpened():
            raise RuntimeError("全局摄像头初始化失败，无法创建DogClient实例")

    def recv_exact(self, n: int) -> bytes:
        buf = b""
        while len(buf) < n:
            chunk = self.client_socket.recv(n - len(buf))
            if not chunk:
                raise ConnectionError("服务器连接已断开")
            buf += chunk
        return buf

    def recv_all(self) -> bytes:
        len_buf = self.recv_exact(4)
        (data_size,) = struct.unpack(">I", len_buf)
        return self.recv_exact(data_size)

    def connect(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(self.timeout)
            self.client_socket.connect((self.host, self.port))
            self.running = True
            if self.debug:
                print(f"✅ 已连接到服务器 {self.host}:{self.port}")
            return True
        except socket.timeout:
            if self.debug:
                print(f"❌ 连接超时（{self.timeout}s），请检查服务器是否在线")
        except ConnectionRefusedError:
            if self.debug:
                print(f"❌ 连接被拒绝，请检查服务器是否启动/端口是否正确")
        except Exception as e:
            if self.debug:
                print(f"❌ 连接失败: {e}")
        return False

    def send_frame(self):
        # 新增编码参数
        encode_param = [cv2.IMWRITE_JPEG_QUALITY, 80]
        while self.running and self.client_socket is not None:
            try:
                # 修改：使用全局摄像头获取帧
                success, frame = self.camera.get_frame()
                if not success:
                    if self.debug:
                        print("⚠️  未获取到有效图像帧")
                    time.sleep(0.05)
                    continue
                
                # 修改：添加时间文本
                cv2.putText(
                    frame,
                    f"Time: {time.strftime('%H:%M:%S')}",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )
                
                # 修改：编码为JPEG
                _, img_encoded = cv2.imencode('.jpg', frame, encode_param)
                frame_data = img_encoded.tobytes()
                
                if frame_data and self.client_socket:
                    frame_len = len(frame_data)
                    self.client_socket.sendall(frame_len.to_bytes(4, byteorder='big'))
                    self.client_socket.sendall(frame_data)
                    
                    if self.debug and frame_len > 0:
                        print(f"📤 发送帧数据: {frame_len} bytes")

                    reply_bytes = self.recv_all()
                    reply = json.loads(reply_bytes.decode("utf-8"))
                    
                    if reply["status"] == "success":
                        cls_idx_list = [obj["class_id"] for obj in reply["detected_objects"]]
                        print(f"\n📥 推理结果 | 耗时: {reply['inference_ms']}ms")
                        print(f"🔍 检测到的cls_idx列表: {cls_idx_list}")
                        
                        # 统计5和6的数量
                        count_5 = cls_idx_list.count(5)
                        count_6 = cls_idx_list.count(6)
                        total_5_6 = count_5 + count_6
                        
                        # 先播报所有目标
                        for idx, obj in enumerate(reply["detected_objects"]):
                            print(f"  目标{idx+1} | cls_idx: {obj['class_id']} | 类别: {CLASS_NAMES[obj['class_id']]} | 置信度: {obj['confidence']}")
                            asyncio.run(play_speech_directly(CLASS_CN_MAP[obj['class_id']]))
                            time.sleep(2)
                        
                        # 如果有检测到5或6，额外播报统计信息
                        if total_5_6 > 0:
                            stats_text = f"共检测到{total_5_6}个安全帽相关目标，其中未佩戴安全帽{count_5}个，佩戴安全帽{count_6}个"
                            print(f"📊 统计信息: {stats_text}")
                            asyncio.run(play_speech_directly(stats_text))
                            time.sleep(2)
                    else:
                        print(f"❌ 服务器返回错误: {reply['msg']}")
                
                time.sleep(0.05)  # 调整发送间隔
            except BrokenPipeError:
                if self.debug:
                    print("❌ 服务器断开连接，停止发送帧")
                self.running = False
                break
            except ConnectionError as e:
                if self.debug:
                    print(f"❌ 连接异常: {e}")
                self.running = False
                break
            except Exception as e:
                if self.debug:
                    print(f"⚠️  发送/接收帧失败: {e}")
                time.sleep(0.5)

    def stop(self):
        self.running = False
        # 关闭socket
        if self.client_socket:
            try:
                self.client_socket.shutdown(socket.SHUT_RDWR)
                self.client_socket.close()
            except:
                pass
        # 核心修改：不再释放摄像头（由全局管理）
        if self.debug:
            print("✅ 客户端已停止，资源已释放")

    def start(self):
        # 检查相机是否可用
        if not self.camera or not self.camera.isOpened():
            if self.debug:
                print("❌ 相机初始化失败或不可用，退出程序")
            return
        
        # 连接服务器
        if not self.connect():
            return  # 不再释放摄像头
        
        # 启动发送帧线程
        frame_thread = threading.Thread(target=self.send_frame, daemon=True)
        frame_thread.start()
        
        # 主线程保持运行
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            if self.debug:
                print("\n🛑 用户中断程序")
        finally:
            self.stop()

if __name__ == "__main__":
    client = DogClient(
        host='172.18.17.47',  
        port=5555,             
        debug=True
    )
    client.start()