# Supplier:

# 0-9:       210, 963
# 10-146:    1040,6711
# 147-583:   6738, 21064
# 584-20000: 21092, 32452

import numpy as np
import os

# Define the four min/max ID ranges
ranges = [
    (210, 963),   # set1: index 0-9
    (1040, 6711),   # set2: index 10-146
    (6738, 21064),   # set3: index 147-583
    (21092, 32452),   # set4: index 584-20000
]

# Output directory for saving .npy files
output_dir = "generated_sets"
os.makedirs(output_dir, exist_ok=True)

# Generate and save 4 files for each range
for i, (global_min, global_max) in enumerate(ranges, start=1):
    for j in range(1, 5):
        # Generate 1000 random numbers uniformly in the range
        generated_numbers = np.random.uniform(global_min, global_max, 1000)
        # Sort the numbers
        sorted_numbers = np.sort(generated_numbers)
        # Save to .npy file
        filename = f"set{i}-{j}.npy"
        filepath = os.path.join(output_dir, filename)
        np.save(filepath, sorted_numbers)

print(f"All 16 files saved in '{output_dir}' directory.")
