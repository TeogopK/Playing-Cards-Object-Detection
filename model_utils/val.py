from ultralytics import YOLO

if __name__ == "__main__":

    model = YOLO('runs/detect/train/weights/best.pt')

    metrics = model.val(data='dataset_combined/data.yaml')