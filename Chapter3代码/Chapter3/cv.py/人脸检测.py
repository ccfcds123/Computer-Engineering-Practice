import cv2

# ===================== 配置项 =====================
IMAGE_PATH = "/home/pi/Pictures/OIP-C.jpg"  # 待检测的图片路径
SAVE_PATH = "/home/pi/Pictures/face_detected.jpg"  # 检测结果保存路径
# Haar分类器路径（适配OpenCV所有版本）
CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'

def detect_face_and_save():
    # 2. 加载Haar特征分类器
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
    if face_cascade.empty():
        print(f"❌ 错误：Haar分类器加载失败 → {CASCADE_PATH}")
        return
    print("✅ Haar人脸分类器加载成功")
    
    # 3. 读取图像
    image = cv2.imread(IMAGE_PATH)
    if image is None:
        print(f"❌ 错误：无法读取图片 → {IMAGE_PATH}")
        return
    print(f"✅ 成功读取图片：{IMAGE_PATH}（尺寸：{image.shape[1]}×{image.shape[0]}）")
    
    # 4. 转换为灰度图像
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 5. 进行人脸检测
    faces = face_cascade.detectMultiScale(
        gray_image, 
        scaleFactor=1.1, 
        minNeighbors=5, 
        minSize=(30, 30)
    )
    print(f"🔍 检测到 {len(faces)} 个人脸")
    
    # 6. 绘制检测框
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        print(f"📌 人脸位置：左上角({x},{y})，宽{w}，高{h}")
    
    # 7. 保存检测结果（核心：替代imshow显示）
    cv2.imwrite(SAVE_PATH, image)
    print(f"✅ 检测结果已保存到：{SAVE_PATH}")

if __name__ == "__main__":
    detect_face_and_save()