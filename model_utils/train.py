"""
Performs training with the specified pretrained model and dataset yaml configuration file.
"""
from ultralytics import YOLO


DATASET_NAME = 'real_dataset'
BASE_MODEL = 'yolov8m_synthetic.pt'

# Change the train and val to absolute paths in the yaml file or change the running directory if there are exceptions.
DATASET_CONFIGURATION_PATH = f'./data/{DATASET_NAME}/data.yaml'
PRETRAINED_MODEL_PATH = f'../final_models/{BASE_MODEL}'
SAVE_DIR = f'../runs'

if __name__ == "__main__":
    model = YOLO(PRETRAINED_MODEL_PATH)

    model.train(data=DATASET_CONFIGURATION_PATH, imgsz=640,
                epochs=10, workers=1, save_dir=SAVE_DIR)
