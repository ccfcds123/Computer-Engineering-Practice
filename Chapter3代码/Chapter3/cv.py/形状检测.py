import cv2
import numpy as np

# 1. 读取图像
img = cv2.imread("/home/pi/Pictures/contour.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("/home/pi/Pictures/contour_gray.png",gray)

# 2. 二值化
_, thresh = cv2.threshold(gray, 130, 255, cv2.THRESH_BINARY)
cv2.imwrite("/home/pi/Pictures/contour_thresh.png",thresh)

# 3. 提取轮廓
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 4. 遍历轮廓识别形状
for contour in contours:
    perim_px = cv2.arcLength(contour, True)
    epsilon = 0.02 * perim_px
    approx = cv2.approxPolyDP(contour, epsilon, True)

    # 绘制轮廓
    cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)

    # 计算中心
    M = cv2.moments(contour)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
    else:
        cx, cy = 0, 0

    # 判断形状
    sides = len(approx)
    shape = "Unknown"
    if sides == 3:
        shape = "Triangle"
    elif sides == 4:
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        shape = "Square" if 0.95 < aspect_ratio < 1.05 else "Rectangle"
    elif sides > 5:
        shape = "Circle"

    # 标注文字
    cv2.putText(img, shape, (cx - 40, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# 5. 直接保存，不显示任何窗口
cv2.imwrite("/home/pi/Pictures/result.png", img)

print("形状检测完成，已保存为 result.png")