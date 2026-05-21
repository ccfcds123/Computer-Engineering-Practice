import os
import random
import shutil
from pathlib import Path

def split_dataset_and_copy_labels():
    """
    将图片按80%/20%划分到train/val目录，并同步复制对应同名的标签文件
    """
    # ------------------- 核心配置（请确认路径正确性） -------------------
    # 源文件路径
    SRC_IMAGES_DIR = r"C:\Users\woshi\Desktop\photos\images"  # 源图片文件夹
    SRC_LABELS_DIR = r"C:\Users\woshi\Desktop\photos\labels"   # 源标签(txt)文件夹
    
    # 目标文件路径
    TARGET_TRAIN_IMAGES = r"C:\Users\woshi\Desktop\yolo_dataset\images\train"  # 训练集图片文件夹
    TARGET_VAL_IMAGES = r"C:\Users\woshi\Desktop\yolo_dataset\images\val"       # 验证集图片文件夹
    TARGET_TRAIN_LABELS = r"C:\Users\woshi\Desktop\yolo_dataset\labels\train"   # 训练集标签文件夹
    TARGET_VAL_LABELS = r"C:\Users\woshi\Desktop\yolo_dataset\labels\val"       # 验证集标签文件夹
    
    # 图片格式（可根据需要扩展）
    IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')
    
    try:
        # 1. 路径初始化：检查源路径+创建目标路径
        src_images_path = Path(SRC_IMAGES_DIR)
        src_labels_path = Path(SRC_LABELS_DIR)
        
        # 检查源图片/标签文件夹是否存在
        if not src_images_path.exists():
            raise FileNotFoundError(f"源图片文件夹不存在: {SRC_IMAGES_DIR}")
        if not src_labels_path.exists():
            raise FileNotFoundError(f"源标签文件夹不存在: {SRC_LABELS_DIR}")
        
        # 创建所有目标文件夹（不存在则创建，存在则不报错）
        for dir_path in [TARGET_TRAIN_IMAGES, TARGET_VAL_IMAGES, TARGET_TRAIN_LABELS, TARGET_VAL_LABELS]:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
        
        # 2. 获取所有源图片文件（过滤非图片格式）
        all_image_files = []
        for file in src_images_path.iterdir():
            if file.is_file() and file.suffix.lower() in IMAGE_EXTENSIONS:
                all_image_files.append(file)
        
        # 检查图片数量
        total_images = len(all_image_files)
        if total_images == 0:
            raise ValueError("源图片文件夹中未找到任何图片文件")
        print(f"共找到 {total_images} 张图片，开始按80%/20%划分...")
        
        # 3. 随机打乱图片列表（保证划分随机性）
        random.shuffle(all_image_files)
        
        # 4. 计算划分数量（80%作为train，剩余作为val）
        train_count = int(total_images * 0.8)
        train_images = all_image_files[:train_count]
        val_images = all_image_files[train_count:]
        
        print(f"划分结果：训练集 {len(train_images)} 张，验证集 {len(val_images)} 张")
        
        # ------------------- 复制图片文件 -------------------
        # 复制train图片
        print("\n=== 开始复制训练集图片 ===")
        for img_file in train_images:
            dest_file = Path(TARGET_TRAIN_IMAGES) / img_file.name
            shutil.copy2(img_file, dest_file)
            print(f"复制图片: {img_file.name} -> {TARGET_TRAIN_IMAGES}")
        
        # 复制val图片
        print("\n=== 开始复制验证集图片 ===")
        for img_file in val_images:
            dest_file = Path(TARGET_VAL_IMAGES) / img_file.name
            shutil.copy2(img_file, dest_file)
            print(f"复制图片: {img_file.name} -> {TARGET_VAL_IMAGES}")
        
        # ------------------- 复制对应标签文件 -------------------
        def copy_corresponding_labels(image_list, target_label_dir, set_name):
            """
            根据图片列表复制对应标签文件
            """
            missing_labels = []
            copied_count = 0
            
            print(f"\n=== 开始复制{set_name}集标签 ===")
            for img_file in image_list:
                # 图片名去掉后缀 = 标签文件名（如：cat.jpg -> cat.txt）
                label_filename = img_file.stem + ".txt"
                src_label_file = src_labels_path / label_filename
                dest_label_file = Path(target_label_dir) / label_filename
                
                if src_label_file.exists():
                    shutil.copy2(src_label_file, dest_label_file)
                    copied_count += 1
                    print(f"复制标签: {label_filename} -> {target_label_dir}")
                else:
                    missing_labels.append(label_filename)
            
            # 提示缺失的标签文件
            if missing_labels:
                print(f"\n⚠️  警告：以下{set_name}集标签文件未找到：")
                for label in missing_labels:
                    print(f"  - {label}")
            return copied_count, missing_labels
        
        # 复制train标签
        train_label_count, train_missing = copy_corresponding_labels(train_images, TARGET_TRAIN_LABELS, "训练")
        
        # 复制val标签
        val_label_count, val_missing = copy_corresponding_labels(val_images, TARGET_VAL_LABELS, "验证")
        
        # ------------------- 输出最终统计 -------------------
        print("\n" + "="*50)
        print("数据集划分完成！最终统计：")
        print(f"📸 图片：训练集 {len(train_images)} 张 | 验证集 {len(val_images)} 张")
        print(f"🏷️  标签：训练集 {train_label_count} 个 | 验证集 {val_label_count} 个")
        if train_missing or val_missing:
            print(f"⚠️  缺失标签：训练集 {len(train_missing)} 个 | 验证集 {len(val_missing)} 个")
        print("="*50)
        
    except Exception as e:
        print(f"\n❌ 程序执行出错：{str(e)}")

if __name__ == "__main__":
    # 固定随机种子（可选：如果需要每次划分结果一致，取消下面注释）
    # random.seed(42)
    split_dataset_and_copy_labels()