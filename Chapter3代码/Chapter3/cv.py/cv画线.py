import cv2
import numpy as np

# ===================== 配置参数（可直接修改） =====================
WIDTH, HEIGHT = 512, 512  # 画布尺寸
BG_COLOR = (0, 0, 0)       # 背景色（BGR）：黑色
SAVE_PATH = ""  # 保存路径（可改绝对路径，如"/home/pi/drawing.png"）

# ===================== 创建画布 =====================
# 创建指定尺寸的黑色背景图（3通道，uint8类型）
img = np.full((HEIGHT, WIDTH, 3), BG_COLOR, dtype=np.uint8)

# ===================== 绘制形状 =====================
# 1. 绘制绿色直线（起点→终点，线宽3）
cv2.line(img, (50, 100), (450, 100), (0, 255, 0), thickness=3)

# 2. 绘制蓝色矩形（左上角→右下角，线宽2，-1为填充）
cv2.rectangle(img, (100, 150), (400, 300), (255, 0, 0), thickness=2)

# 3. 绘制红色实心圆（圆心，半径，实心）
cv2.circle(img, (256, 400), 50, (0, 0, 255), thickness=-1)

# 4. 绘制青色椭圆（中心点，长短轴，旋转角度，起始/终止角度，线宽2）
cv2.ellipse(img, (256, 256), (100, 50), 45, 0, 360, (255, 255, 0), 2)

# 5. 绘制白色多边形（顶点坐标，闭合，线宽2）
pts = np.array([[100,400], [200,350], [300,400], [250,450], [150,450]], np.int32)
pts = pts.reshape((-1, 1, 2))  # 转换为OpenCV要求的形状：(点数, 1, 2)
cv2.polylines(img, [pts], isClosed=True, color=(255, 255, 255), thickness=2)

# 6. 添加黄色文字（抗锯齿，更清晰）
cv2.putText(
    img, 
    "2026.03.12 OpenCV Drawing Demo", 
    (50, 50),                # 文本左下角坐标
    cv2.FONT_HERSHEY_SIMPLEX, # 字体
    1,                       # 字体大小
    (0, 255, 255),           # 颜色：黄色
    2,                       # 线宽
    cv2.LINE_AA              # 抗锯齿
)

# ===================== 保存绘制结果 =====================
# 保存图片到指定路径，并检查是否保存成功
save_success = cv2.imwrite("/home/pi/Pictures/cvplotfigure.jpg", img)
if save_success:
    print(f"绘制完成！图片已保存至：{SAVE_PATH}")
else:
    print(f"保存失败！请检查路径 {SAVE_PATH} 是否有写入权限，或路径是否合法。")