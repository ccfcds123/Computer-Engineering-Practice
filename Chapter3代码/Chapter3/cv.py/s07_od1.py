import cv2
import os

# ===================== 配置项（只需改这3处） =====================
VIDEO_PATH = "/home/pi/xgoVideos/stree.mp4"  # 机器狗本地视频路径
SAVE_PATH = "/home/pi/xgoVideos/stree_track.mp4"  # 追踪结果保存路径
TRACKER_TYPE = "CSRT"  # 追踪器：CSRT（精准）/KCF（快速，适合树莓派）

# ===================== 核心：创建追踪器 =====================
def create_tracker(tracker_type):
    if tracker_type == "CSRT":
        return cv2.legacy.TrackerCSRT_create()
    elif tracker_type == "KCF":
        return cv2.legacy.TrackerKCF_create()
    else:
        return cv2.legacy.TrackerCSRT_create()

# ===================== 主函数：视频追踪并保存结果 =====================
def track_human_and_save():
    # 1. 检查视频文件是否存在
    if not os.path.exists(VIDEO_PATH):
        print(f"❌ 错误：视频文件不存在 → {VIDEO_PATH}")
        print("请确认视频已上传到机器狗的对应目录！")
        return

    # 2. 打开视频
    cap = cv2.VideoCapture(VIDEO_PATH)
    if not cap.isOpened():
        print(f"❌ 错误：无法打开视频 → {VIDEO_PATH}")
        return
    print(f"✅ 成功打开视频：{VIDEO_PATH}")

    # 3. 获取视频参数（用于保存结果）
    fps = int(cap.get(cv2.CAP_PROP_FPS))  # 视频帧率
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 宽度
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 高度
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 保存格式（MP4）
    out = cv2.VideoWriter(SAVE_PATH, fourcc, fps, (width, height))

    # 4. 读取第一帧，手动ROI改为「固定初始框」（适配无界面）
    ret, frame = cap.read()
    if not ret:
        print("❌ 错误：无法读取视频第一帧")
        cap.release()
        out.release()
        return
    
    # 关键适配：机器狗无界面，手动ROI改为「固定初始框」（可根据视频调整）
    # 格式：(x, y, w, h) → 示例：画面中心偏左，宽200，高300（可根据你的视频调整）
    bbox = (width//3, height//4, 200, 300)
    print(f"⚠️ 使用固定初始追踪框：{bbox}（可根据视频调整代码中的bbox值）")

    # 5. 初始化追踪器
    tracker = create_tracker(TRACKER_TYPE)
    ok = tracker.init(frame, bbox)
    if not ok:
        print("❌ 错误：追踪器初始化失败")
        cap.release()
        out.release()
        return

    # 6. 逐帧追踪并保存结果
    frame_count = 0
    print("✅ 开始追踪并保存结果...")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("✅ 视频追踪完成！")
                break

            # 更新追踪结果
            ok, bbox = tracker.update(frame)

            # 绘制追踪框
            if ok:
                x, y, w, h = map(int, bbox)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, "Tracking", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                frame_count += 1
                if frame_count % 10 == 0:  # 每10帧打印一次进度
                    print(f"📌 已处理 {frame_count} 帧 | 目标位置：({x}, {y}, {w}, {h})")
            else:
                cv2.putText(frame, "Lost", (20, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                print(f"❌ 第 {frame_count} 帧：追踪丢失")

            # 写入追踪后的帧到新视频
            out.write(frame)

    except KeyboardInterrupt:
        print("\n🛑 用户手动终止追踪")
    finally:
        # 7. 释放资源
        cap.release()
        out.release()
        print(f"✅ 追踪结果已保存到：{SAVE_PATH}")
        print(f"📊 总计处理 {frame_count} 帧")

# ===================== 运行入口 =====================
if __name__ == "__main__":
    track_human_and_save()
