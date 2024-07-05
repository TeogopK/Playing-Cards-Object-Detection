"""
Executes the latest running model on the test set.

The test set must be defined in the yaml configuration file as a 'val' set.
Make sure the path to the model includes the 'train' directory and not 'train2', 3, etc.
Changed it if needed.
"""

from ultralytics import YOLO

DATASET_NAME = 'real_dataset'

if __name__ == "__main__":
    model = YOLO('../runs/detect/train/weights/best.pt')

    metrics = model.val(data=f'./data/{DATASET_NAME}/test.yaml')
