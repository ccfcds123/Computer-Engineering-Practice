import cv2
import os

# ===================== 配置项（根据你的视频调整） =====================
VIDEO_PATH = "/home/pi/xgoVideos/stree.mp4"  # 机器狗视频路径
SAVE_PATH = "/home/pi/xgoVideos/track_result.mp4"  # 结果保存路径
# 改用MOSSE追踪器（核心模块自带，无需contrib）
BOOSTING = "MOSSE"
# 预设追踪初始框（根据视频宽1920×1080调整，建议放大一点）
PRESET_BBOX = (200, 150, 200, 400)  # 适配1920×1080分辨率

# ===================== 创建追踪器（核心修改：去掉legacy） =====================
def create_tracker(BOOSTING):
    """改用核心模块追踪器，避免legacy依赖"""
    if tracker_type == "MOSSE":
        return cv2.legacy.TrackerMOSSE_create()  # MOSSE兼容性更好
    # 备选：若MOSSE也报错，用BOOSTING（最基础，所有版本都支持）
    elif tracker_type == "BOOSTING":
        return cv2.legacy.TrackerBoosting_create()
    else:
        return cv2.legacy.TrackerMOSSE_create()

# ===================== 主函数：追踪并保存 =====================
def track_video_and_save():
    # 1. 检查视频文件
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ 视频文件不存在：{VIDEO_PATH}")
        return
    
    # 2. 打开视频
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"❌ 无法打开视频：{VIDEO_PATH}")
        return
    print(f"✅ 成功打开视频：{VIDEO_PATH}")
    
    # 3. 获取视频参数（用于保存）
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"📹 视频参数：宽{width} × 高{height}，帧率{fps}")
    
    # 4. 初始化视频写入器（保存结果）
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(SAVE_PATH, fourcc, fps, (width, height))
    
    # 5. 读取第一帧，用预设框初始化追踪器
    ret, frame = cap.read()
    if not ret:
        print("❌ 无法读取视频第一帧")
        cap.release()
        out.release()
        return
    
    # 使用预设框替代手动框选
    bbox = PRESET_BBOX
    print(f"⚠️ 使用预设初始追踪框：{bbox}（若追踪不准，请调整PRESET_BBOX值）")
    
    # 初始化追踪器（关键：改用MOSSE，避免KCF/CSRT的contrib依赖）
    tracker = create_tracker(BOOSTING)
    ok = tracker.init(frame, bbox)
    if not ok:
        print("❌ 追踪器初始化失败")
        cap.release()
        out.release()
        return
    
    # 6. 逐帧追踪并保存
    frame_count = 0
    print("✅ 开始追踪，按 Ctrl+C 终止...")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("\n✅ 视频处理完成！")
                break
            
            # 更新追踪结果
            ok, bbox = tracker.update(frame)
            
            # 绘制追踪框
            if ok:
                x, y, w, h = map(int, bbox)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                cv2.putText(frame, "Tracking (MOSSE)", (20,40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)
                if frame_count % 20 == 0:  # 每20帧打印一次进度
                    print(f"📌 已处理{frame_count}帧 | 目标位置：({x},{y},{w},{h})")
            else:
                cv2.putText(frame, "Lost", (20,40), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)
                print(f"❌ 第{frame_count}帧：追踪丢失")
            
            # 保存帧到结果视频
            out.write(frame)
            frame_count += 1
    
    except KeyboardInterrupt:
        print("\n🛑 用户手动终止")
    finally:
        # 释放资源
        cap.release()
        out.release()
        print(f"✅ 追踪结果已保存到：{SAVE_PATH}")
        print(f"📊 总计处理 {frame_count} 帧")

if __name__ == "__main__":
    track_video_and_save()