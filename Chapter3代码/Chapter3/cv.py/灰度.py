import cv2

# 图片路径
img_path = "/home/pi/Pictures/ball.jpg"
# 读取图片并做异常判断
img = cv2.imread(img_path)
if img is None:
    print(f"错误：无法读取图片，请检查路径 {img_path} 是否正确/文件是否完好")
else:
    # 彩色转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 关键：不显示，直接保存灰度图（命名加_gray区分原文件）
    save_path = "/home/pi/Pictures/fig1_gray.png"
    cv2.imwrite(save_path, gray)
    print(f"灰度图已成功保存！路径：{save_path}")