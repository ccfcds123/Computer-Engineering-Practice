import cv2

# 1. 配置参数（改这几行就行）
input_path = "/home/pi/Pictures/ball.jpg"    # 你的原图路径
output_path = "/home/pi/Pictures/ball_cut.png"  # 剪裁后的保存路径
row_start, row_end = 100, 400  # 行范围（高度）
col_start, col_end = 100, 400  # 列范围（宽度）

# 2. 读取图片
img = cv2.imread(input_path)

# 3. 核心：剪裁（行范围, 列范围）
cropped_img = img[row_start:row_end, col_start:col_end]

# 4. 保存剪裁结果
cv2.imwrite(output_path, cropped_img)
print(f"剪裁完成！已保存至 {output_path}")