import os
import glob
import numpy as np

# Define the folder where the .npy files are located
folder_path = 'Supplier'  # Replace with the actual folder path

# Find all .npy files in the folder
file_pattern = os.path.join(folder_path, '*.npy')
files = glob.glob(file_pattern)

# Initialize min and max values
global_min = float('inf')
global_max = float('-inf')

# Iterate over the files and find the global min and max
for file_path in files:
    try:
        data = np.load(file_path)
        file_min = data.min()
        file_max = data.max()
        
        if file_min < global_min:
            global_min = file_min
        if file_max > global_max:
            global_max = file_max
        
        print(f'Processed: {file_path} - Min: {file_min}, Max: {file_max}')
    except Exception as e:
        print(f'Error processing {file_path}: {e}')

print(f'Global Min: {global_min}')
print(f'Global Max: {global_max}')

