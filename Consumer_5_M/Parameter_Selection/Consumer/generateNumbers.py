# Consumer:

# 0-9:       105000000, 105000753
# 10-146:    105000830, 105006501
# 147-583:   105006528, 105020854
# 584-20000: 105020882, 105032242

import numpy as np
import os

# Define the four min/max ID ranges
ranges = [
    (105000000, 105000753),   # set1: index 0-9
    (105000830, 105006501),   # set2: index 10-146
    (105006528, 105020854),   # set3: index 147-583
    (105020882, 105032242),   # set4: index 584-20000
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
