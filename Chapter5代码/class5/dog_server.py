import socket
import cv2
import json
import time
import threading
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import struct

# ===================== 配置项 =====================
CONFIDENCE_THRESHOLD = 0.3  # 置信度阈值
MODEL_PATH = r"C:\Users\cc\Desktop\best2.pt"
SERVER_HOST = "0.0.0.0"       # 监听所有网卡
SERVER_PORT = 5555            # 通信端口
# 类别映射（与nd.yaml一致，中文便于查看）
LABELS_CN = ["偏低", "正常", "偏高","35212","10561","没有头盔","头盔","B","D","A","C"]
# =================================================

def send_all(sock: socket.socket, data: bytes):
    """带长度前缀的完整发送（解决粘包问题）"""
    sock.sendall(struct.pack(">I", len(data)) + data)

def recv_exact(sock: socket.socket, n: int) -> bytes:
    """精确接收n字节，确保数据完整"""
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            raise ConnectionError("客户端连接已断开")
        buf += chunk
    return buf

def recv_all(sock: socket.socket) -> bytes:
    """接收完整数据：先读4字节长度，再读对应内容"""
    len_buf = recv_exact(sock, 4)
    (data_size,) = struct.unpack(">I", len_buf)
    return recv_exact(sock, data_size)

# 加载YOLO模型（仅初始化一次，避免重复加载）
model = YOLO(MODEL_PATH)
print(f"✅ YOLO模型 {MODEL_PATH} 加载完成")

def handle_client(conn: socket.socket, addr):
    """处理单个机器狗客户端请求（多线程）"""
    client_id = f"{addr[0]}:{addr[1]}"
    print(f"\n[+] 机器狗客户端已连接: {client_id}")
    try:
        # 1. 接收机器狗发送的图片数据
        img_bytes = recv_all(conn)
        print(f"[{client_id}] 收到图片数据，大小: {len(img_bytes)} 字节")
        
        # 2. 解码图片并执行YOLO推理
        img_np = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("图片解码失败")
        
        t_start = time.time()
        results = model(img, verbose=False)  # 推理（关闭冗余日志）
        detect_objs = []
        
        # 解析推理结果（过滤低置信度目标）
        for r in results:
            for box in r.boxes:
                conf = box.conf[0].item()
                if conf < CONFIDENCE_THRESHOLD:
                    continue
                # 提取目标坐标、置信度、类别
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                cls_idx = int(box.cls[0])
                detect_objs.append({
                    "xyxy": [round(x, 2) for x in [x1, y1, x2, y2]],  # 保留2位小数
                    "confidence": round(conf, 3),
                    "class_id": cls_idx,
                    #"class_name": LABELS_CN[cls_idx]
                })
        
        # 3. 构造返回结果
        latency = round((time.time() - t_start) * 1000, 1)  # 推理耗时（毫秒）
        reply = json.dumps({
            "status": "success",
            "inference_ms": latency,
            "detected_objects": detect_objs,
            "object_count": len(detect_objs)
        }, ensure_ascii=False)  # ensure_ascii=False 支持中文类别名
        
        # 4. 发送结果给机器狗
        send_all(conn, reply.encode("utf-8"))
        print(f"[{client_id}] 推理完成 | 耗时: {latency}ms | 检测到目标数: {len(detect_objs)}")
        print(f"[{client_id}] 返回结果: {reply}")

    except Exception as e:
        # 异常处理：返回错误信息给机器狗
        error_msg = json.dumps({"status": "error", "msg": str(e)}, ensure_ascii=False)
        send_all(conn, error_msg.encode("utf-8"))
        print(f"[!] {client_id} 处理失败: {e}")
    finally:
        conn.close()
        print(f"[-] {client_id} 连接已断开")

if __name__ == "__main__":
    # 启动TCP服务器
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 端口复用
        server_sock.bind((SERVER_HOST, SERVER_PORT))
        server_sock.listen(10)  # 最大监听10个客户端
        print(f"🚀 机器狗YOLO推理服务器已启动 | 监听地址: {SERVER_HOST}:{SERVER_PORT}")
        print("========================================")
        
        # 循环接收客户端连接
        while True:
            conn, addr = server_sock.accept()
            # 每个客户端启动独立线程处理，避免阻塞
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()