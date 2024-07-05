"""
Executes the latest running model on a given image.

Make sure the path to the model includes the 'train' directory and not 'train2', 3, etc.
Changed it if needed.
"""

from ultralytics import YOLO

IMAGE_FILE = '1.jpg'

if __name__ == "__main__":
    model = YOLO('../runs/detect/train/weights/best.pt')

    model.predict(show=True, conf=0.5,
                  source=f"./data/test_images/{IMAGE_FILE}", line_width=1, save=True)
