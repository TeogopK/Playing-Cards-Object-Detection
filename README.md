# Playing-Cards-Object-Detection

This repository contains the code and datasets used for training and evaluating various YOLOv8 models for playing cards object detection. The project includes synthetic and real datasets, augmentation scripts, and trained models.

## Overview

The goal of this project is to detect and classify playing cards using object detection models. The datasets and models are organized to facilitate easy training, validation, and testing.

## Datasets

Playing cards datasets used during the training of the models.
All datasets are in YOLOv8 object detection format, split on *train, valid and test* directories with *labels* and *images* subdirectories.
All of them fall under the [CC0: Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) license.

### The Synthetic dataset

- Copied from [Kaggle - Playing Cards Object Detection Dataset](https://www.kaggle.com/datasets/andy8744/playing-cards-object-detection-dataset)
- Includes 20 000 images synthetically generated and labeled imaged with 52 classes.
- Used to train the *YOLOv8m_synthetic* model.

### The "Real" dataset

- Created by the author of the project - Teodor Kostadinov
- Includes 100 images shot and labelled by the author using [Label Studio](https://labelstud.io/) with 13 classes.
- Used to train the *YOLOv8m_real* and *YOLOv8m_tuned* model.

### The "Real" Augmented dataset

- Created using [imgaug](https://imgaug.readthedocs.io/en/latest/) with the script [augment_dataset.ipynb](./dataset_utils/augment_dataset.ipynb) 
- Introduces 10 augmented images for each image in the "Real" dataset using different transformations.
- Used to train the *YOLOv8m_aug* model.

### The Combined dataset

- Created using [imgaug](https://imgaug.readthedocs.io/en/latest/) with the scripts [combine_datasets.py](./dataset_utils/combine_datasets.py) and [transform_labels_in_dataset.py](./dataset_utils/transform_labels_in_dateset.py)
- Combines the full "Real" Dataset with 10 times more than it taken from the Synthetic dataset.
- Used to train the *YOLOv8m_comb* model.

#### Notes

- To use the datasets, one may need to replace the relative paths provided in the `data.yaml` file.
- The provided`test.yaml` files have the same structure as the `data.yaml` ones but are used to execute the model on the test set. This is done by replacing the path to the validation set with the path to the test set.
- All model runs has old project structure datasets path in the *args* configuration file.

## Models

Within the [runs](./runs) directory, you'll find all the data extracted from the training process of each model. The whole process of training, validating and testing the models is executed using the scripts in [model_utils](./model_utils/).

The table summarizes the models, datasets, epochs, and training times on *NVIDIA RTX A2000 8GB*:

| Model | Dataset | Epochs | Training Time |
| --- | --- | ---- | ---- |
| [YOLOv8m_synthetic](./runs/YOLOv8m_synthetic) | 20,000 synthetic images      | 10     | 2 hours    |
| [YOLOv8m_real](./runs/YOLOv8m_real)      | 100 real images              | 100    | 20 minutes |
| [YOLOv8m_aug](./runs/YOLOv8m_aug)       | 1,000 augmented images       | 100    | 40 minutes |
| [YOLOv8m_comb](./runs/YOLOv8m_comb)      | 100 real + 1,000 synthetic   | 100    | 50 minutes |
| [YOLOv8m_tuned](./runs/YOLOv8m_tuned)     | 100 real images (fine-tuned) | 100    | 10 minutes |

The best models are presented in the directory [final_models](./final_models). They are extracted from each models `'train/weights/best.pt'`.
