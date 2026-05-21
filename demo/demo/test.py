from ultralytics import YOLO
import cv2

# 加载模型
model = YOLO(r"C:\Users\cc\Desktop\Study\大学\计算机工程实践\demo\demo\best.pt")  # 替换为你的模型路径

# 测试图像路径
image_path = r"C:\Users\cc\Desktop\Study\大学\计算机工程实践\demo\demo\D_frame_240.jpg"  # 替换为你的测试图片

# 运行推理
results = model(image_path, conf=0.25)  # 置信度阈值0.25

# 显示结果
for r in results:
    # 打印检测到的目标
    if r.boxes is not None:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            class_name = model.names[cls_id]
            print(f"类别: {class_name} (ID: {cls_id}), 置信度: {conf:.3f}")
    else:
        print("未检测到任何目标")

    # 可视化并保存
    annotated = r.plot()  # 绘制检测框
    cv2.imshow("Result", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()