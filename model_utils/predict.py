from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO('yolov8s_custom.pt')

    model.predict(show=True, conf=0.1, source="32.jpg", line_width=1)
