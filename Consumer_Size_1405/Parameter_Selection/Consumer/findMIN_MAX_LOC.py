
import numpy as np
import os

# Folder containing the .npy files
folder_path = '/Consumer/Consumer/'

# List of locations for minimum and maximum values
min_locations = [0, 9, 10, 146, 147, 583, 584, 5000]
max_locations = [0, 9, 10, 146, 147, 583, 584, 5000]



# Initialize min and max arrays with appropriate values
min_values = [float('inf')] * len(min_locations)
max_values = [-float('inf')] * len(max_locations)

# Iterate over all npy files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.npy'):
        file_path = os.path.join(folder_path, file_name)
        data = np.load(file_path)
        
        # Update minimum values
        for i, loc in enumerate(min_locations):
            min_values[i] = min(min_values[i], data[loc])
        
        # Update maximum values
        for i, loc in enumerate(max_locations):
            max_values[i] = max(max_values[i], data[loc])

# Output the results
print("Minimum values at specified locations:", min_values)
print("Maximum values at specified locations:", max_values)
