import cv2

# 1. 配置路径（根据你的实际情况修改）
# 原图路径（建议用绝对路径，避免找不到文件）
img_path = "/home/pi/Pictures/ball.jpg"
# 缩小版图片的保存路径
small_save_path = "/home/pi/Pictures/fig1_small.png"
# 200x200版图片的保存路径
resize_200x200_save_path = "/home/pi/Pictures/fig1_fix.png"
# 2. 读取图片
img = cv2.imread(img_path)
# 3. 检查图片是否读取成功
if img is None:
    print(f"错误：无法读取图片 {img_path}，请检查文件路径或文件名是否正确！")
else:
    # 4. 调整图片尺寸
    # 方式1：按比例缩小50%（保持原图宽高比）
    small = cv2.resize(img, (0, 0), fx=0.1, fy=0.1)
    # 方式2：强制缩放到200x200像素（可能拉伸/压缩）
    resize_200x200 = cv2.resize(img, (200, 200))

    # 5. 保存调整后的图片（核心修改：替换显示为保存）
    # 保存缩小版
    cv2.imwrite(small_save_path, small)
    # 保存200x200版
    cv2.imwrite(resize_200x200_save_path, resize_200x200)

    # 打印提示，确认保存成功
    print(f"图片保存完成！")
    print(f"- 缩小50%的图片：{small_save_path}")
    print(f"- 200x200尺寸的图片：{resize_200x200_save_path}")
