from ultralytics import YOLO
if __name__ == "__main__":
    model = YOLO(r"C:\Users\cc\Desktop\Study\大学\计算机工程实践\Chapter5代码\class5\yolo_dataset\yolo11n.pt")  #预训练模型或路径
    model.train(
        data=r"C:\Users\cc\Desktop\Study\大学\计算机工程实践\Chapter5代码\class5\yolo_dataset\yolo_dataset.yaml",  #yaml文件路径
        epochs=100, 
        imgsz=640,
        batch=-1,
        device=0,
        save=True
        )