import cv2
# 读取图像并去噪（关键：Canny前去噪能大幅提升效果）
img = cv2.imread("/home/pi/Pictures/ball.jpg", 0)  # 0表示读取为灰度图（边缘检测无需彩色）
img_blur = cv2.GaussianBlur(img, (3,3), 0)

# Canny边缘检测
edges = cv2.Canny(img_blur, 100, 200)

#Sobel 算子
sobel_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
sobel_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=5)

sobel_x_abs = cv2.convertScaleAbs(sobel_x)
sobel_y_abs = cv2.convertScaleAbs(sobel_y)
sobel_combined = cv2.addWeighted(sobel_x_abs, 0.5, sobel_y_abs, 0.5, 0)

#laplacian 算子
laplacian = cv2.Laplacian(img_blur, cv2.CV_64F, ksize=3)
laplacian_abs = cv2.convertScaleAbs(laplacian)


# 显示对比
cv2.imwrite("/home/pi/Pictures/ball(canny).jpg", edges)
cv2.imwrite("/home/pi/Pictures/ball(sobel_x).jpg", sobel_x_abs)
cv2.imwrite("/home/pi/Pictures/ball(sobel_y).jpg", sobel_y_abs)
cv2.imwrite("/home/pi/Pictures/ball(sobel_combine).jpg", sobel_combined)
cv2.imwrite("/home/pi/Pictures/ball(laplacian_abs).jpg", laplacian_abs)