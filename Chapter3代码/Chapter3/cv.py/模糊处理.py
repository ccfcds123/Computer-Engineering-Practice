import cv2
import numpy as np

img = cv2.imread("/home/pi/Pictures/crowd.jpeg")

#执行三种模糊处理（核大小建议用奇数，如3/5/7，越大模糊越强）
# 高斯模糊：参数(5,5)是核大小，0是X方向标准差（自动计算）
gaussian_blur = cv2.GaussianBlur(img, (5, 5), 0)
# 均值模糊：参数(5,5)是核大小，邻域内像素取平均
mean_blur = cv2.blur(img, (5, 5))
# 中值模糊：参数5是核大小，邻域内像素取中值（无核大小元组）
median_blur = cv2.medianBlur(img, 5)

#保存处理后的图像（可选，便于后续分析
cv2.imwrite("/home/pi/Pictures/gaussian_blur.jpg", gaussian_blur)
cv2.imwrite("/home/pi/Pictures/mean_blur.jpg", mean_blur)
cv2.imwrite("/home/pi/Pictures/median_blur.jpg", median_blur)

print("图像已保存")