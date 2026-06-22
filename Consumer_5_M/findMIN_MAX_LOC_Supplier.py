import numpy as np
from pathlib import Path
import os

# Folder containing the .npy files

# folder_path = Path("Consumer/")
folder_path = Path("Supplier/")

# List of locations for minimum and maximum values
min_locations = [0, 9, 10, 146, 147, 583, 584, 5000, 10000, 15000, 20000]
max_locations = [0, 9, 10, 146, 147, 583, 584, 5000, 10000, 15000, 20000]


# Initialize min and max arrays with appropriate values
min_values = [float('inf')] * len(min_locations)
max_values = [-float('inf')] * len(max_locations)

# Iterate over all npy files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('1.npy'):
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


# Consumer:

# 0-9:       105000000, 105000753
# 10-146:    105000830, 105006501
# 147-583:   105006528, 105020854
# 584-20000: 105020882, 105032242

# Supplier:

# 0-9:       210, 963
# 10-146:    1040,6711
# 147-583:   6738, 21064
# 584-20000: 21092, 32452
