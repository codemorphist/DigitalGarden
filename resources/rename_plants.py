import os
from tools.planticus import random_name

def rename_files_in_folder(folder_path):
    """Rename all files in the given folder with random names."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(filename)[1]
            new_name = random_name() + file_extension
            new_file_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_file_path)
            print(f'Renamed: {file_path} to {new_file_path}')

# Specify the folder path
folder_path = './orangery/'

# Rename files
rename_files_in_folder(folder_path)

