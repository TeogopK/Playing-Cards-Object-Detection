"""
Combines two YOLOv8 datasets into a new one. Intended to merge small dataset to a percent of the larger.

The script iterates over each train, test, validation directory with subdirectory labels and images.
Takes each content of the first dataset, copies it into the new dataset.
Then takes N times more data from the second dataset compared to the one in the first dataset per each subdirectory.
And copies the taken data into the new location.
"""

import os
import shutil

# NOTE: Change the directories to match the desired datasets
MULTIPLIER = 10
PARENT_DIR = '../data'

dataset1_dir = f'{PARENT_DIR}/real_dataset'
dataset2_dir = f'{PARENT_DIR}/synthetic_dataset'
combined_dataset_dir = f'{PARENT_DIR}/combined' # NOTE: Change the output dir if needed

# Subfolders for train, test, val
folders = ['train', 'test', 'valid']
subfolders = ['images', 'labels']

# Create combined dataset directories
for folder in folders:
    for subfolder in subfolders:
        os.makedirs(os.path.join(combined_dataset_dir,
                    folder, subfolder), exist_ok=True)

# Function to copy files from source to destination


def copy_files(src_dir, dest_dir, num_files):
    files = os.listdir(src_dir)
    files.sort()
    selected_files = files[:num_files]
    for file in selected_files:
        src_path = os.path.join(src_dir, file)
        dest_path = os.path.join(dest_dir, file)
        shutil.copy(src_path, dest_path)


# Combine datasets
for folder in folders:
    for subfolder in subfolders:
        src1 = os.path.join(dataset1_dir, folder, subfolder)
        src2 = os.path.join(dataset2_dir, folder, subfolder)
        dest = os.path.join(combined_dataset_dir, folder, subfolder)

        # Number of files in the first dataset
        num_files_in_src1 = len(os.listdir(os.path.join(src1)))

        # Copy all files from the first dataset
        copy_files(src1, dest, num_files_in_src1)

        # Copy scaled number of files from the second dataset
        num_files_to_copy_from_src2 = num_files_in_src1 * MULTIPLIER
        copy_files(src2, dest, num_files_to_copy_from_src2)

print("Datasets combined successfully.")
