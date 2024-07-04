"""
Script that relabels dataset in YOLOv8 format based on new specified classes.
If some of the old labels do not exist in the current dataset, remove any detected objects of these class in the labels files.
"""

import os

# Old class names
old_class_names = [
    '10c', '10d', '10h', '10s', '2c', '2d', '2h', '2s', '3c', '3d', '3h', '3s',
    '4c', '4d', '4h', '4s', '5c', '5d', '5h', '5s', '6c', '6d', '6h', '6s',
    '7c', '7d', '7h', '7s', '8c', '8d', '8h', '8s', '9c', '9d', '9h', '9s',
    'Ac', 'Ad', 'Ah', 'As', 'Jc', 'Jd', 'Jh', 'Js', 'Kc', 'Kd', 'Kh', 'Ks',
    'Qc', 'Qd', 'Qh', 'Qs'
]

# New class names
new_class_names = ['10h', '2h', '3h', '4h', '5h',
                   '6h', '7h', '8h', '9h', 'Ah', 'Jh', 'Kh', 'Qh']

# Create a mapping from old to new class indices
old_to_new_class_index = {old_class_names.index(
    name): new_class_names.index(name) for name in new_class_names}

# Directories
dataset_base_dir = '../data/combined'  # NOTE: Change the output dir if needed
subdirs = ['train', 'test', 'valid']


def transform_labels(label_path, old_to_new_class_index):
    with open(label_path, 'r') as file:
        lines = file.readlines()

    new_labels = []
    for line in lines:
        parts = line.strip().split()
        old_class_index = int(parts[0])
        if old_class_index in old_to_new_class_index:
            new_class_index = old_to_new_class_index[old_class_index]
            new_labels.append(f"{new_class_index} {' '.join(parts[1:])}\n")

    with open(label_path, 'w') as file:
        file.writelines(new_labels)


# Iterate through all subdirectories and transform labels
for subdir in subdirs:
    label_dir = os.path.join(dataset_base_dir, subdir, 'labels')
    for root, _, files in os.walk(label_dir):
        for file in files:
            if file.endswith('.txt') and '.rf.' in file:  # NOTE specific for dataset
                print(file)
                label_path = os.path.join(root, file)
                transform_labels(label_path, old_to_new_class_index)

print("Labels transformed successfully.")
