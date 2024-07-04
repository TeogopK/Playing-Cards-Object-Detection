from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO('yolo8m_synthetic.pt')

    model.train(data="my_dataset_labeled/data.yaml", imgsz=640, epochs=100, workers=1)
