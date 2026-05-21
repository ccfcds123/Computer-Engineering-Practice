import cv2
import os
import glob

def video_to_frames(video_path, output_dir, frame_interval=10):
    """
    将单个视频文件按指定间隔截取帧保存为图片（统一保存到单个文件夹）
    
    Args:
        video_path: 视频文件路径
        output_dir: 图片输出文件夹（所有视频的帧都保存在此）
        frame_interval: 帧截取间隔（每隔多少帧截取一张，默认10帧）
    """
    # 获取视频文件名（不含扩展名），用于区分不同视频的帧
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频文件: {video_path}")
        return
    
    # 获取视频基本信息
    fps = cap.get(cv2.CAP_PROP_FPS)  # 视频帧率
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # 总帧数
    print(f"正在处理视频: {video_name} | 帧率: {fps} | 总帧数: {total_frames}")
    
    frame_count = 0  # 当前帧计数器
    saved_count = 0  # 已保存图片计数器
    
    while True:
        # 读取一帧
        ret, frame = cap.read()
        if not ret:
            break  # 读取完毕，退出循环
        
        # 按指定间隔保存帧
        if frame_count % frame_interval == 0:
            # 图片保存路径（格式：视频名_帧数.jpg，确保文件名唯一）
            frame_filename = f"{video_name}_frame_{frame_count}.jpg"
            frame_path = os.path.join(output_dir, frame_filename)
            
            # 保存图片
            cv2.imwrite(frame_path, frame)
            saved_count += 1
        
        frame_count += 1
    
    # 释放视频资源
    cap.release()
    print(f"视频 {video_name} 处理完成！共保存 {saved_count} 张图片\n")

def batch_process_videos(input_dir, output_dir, frame_interval=10):
    """
    批量处理指定文件夹下的所有视频（所有帧统一保存到单个文件夹）
    
    Args:
        input_dir: 视频源文件夹路径
        output_dir: 图片输出文件夹（所有帧的统一保存路径）
        frame_interval: 帧截取间隔
    """
    # 创建输出文件夹（如果不存在）
    os.makedirs(output_dir, exist_ok=True)
    
    # 支持的视频格式（可根据需要扩展）
    video_extensions = ["*.mp4", "*.avi", "*.mov", "*.mkv", "*.flv", "*.wmv"]
    
    # 遍历所有视频文件
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(input_dir, ext)))
    
    if not video_files:
        print(f"在 {input_dir} 路径下未找到任何视频文件！")
        return
    
    print(f"共找到 {len(video_files)} 个视频文件，开始批量处理...\n")
    
    # 逐个处理视频
    for video_file in video_files:
        try:
            video_to_frames(video_file, output_dir, frame_interval)
        except Exception as e:
            print(f"处理视频 {video_file} 时出错: {str(e)}\n")

if __name__ == "__main__":
    # 配置路径和参数
    INPUT_VIDEO_DIR = r"C:\Users\cc\Desktop\YOLO"  # 视频源路径
    OUTPUT_PHOTO_DIR = r"C:\Users\cc\Desktop\YOLO\images"      # 所有图片的统一保存路径
    FRAME_INTERVAL = 10  # 每隔10帧截取一张（可根据需要调整）
    
    # 执行批量处理
    batch_process_videos(INPUT_VIDEO_DIR, OUTPUT_PHOTO_DIR, FRAME_INTERVAL)
    print("所有视频处理完成！")