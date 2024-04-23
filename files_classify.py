import os
import shutil

# Define the source directory
source_directory = "dir"

# Define the destination directory
destination_directory = "A"

# Define the keys for classification
keys = {"A", "B", "C", ...}

# Iterate over the files in the source directory
for filename in os.listdir(source_directory):
    # Get the key for the file
    key = filename.split("_")[
        0
    ]  # Assuming the key is the part before the first underscore

    # Check if the destination directory for the key exists, if not, create it
    key_directory = os.path.join(destination_directory, key)
    if not os.path.exists(key_directory):
        os.makedirs(key_directory)

    # Move the file to the destination directory
    source_path = os.path.join(source_directory, filename)
    destination_path = os.path.join(key_directory, filename)
    shutil.move(source_path, destination_path)
