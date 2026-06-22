import numpy as np
import matplotlib.pyplot as plt
import glob

# Function to read data from .npy files at specified indices
def read_data_at_indices(file_pattern, index_ranges):
    data_by_range = {range_key: [] for range_key in index_ranges}
    for filename in glob.glob(file_pattern):
        data = np.load(filename)
        for range_key, (start_idx, end_idx) in index_ranges.items():
            data_by_range[range_key].extend(data[start_idx:end_idx+1])
    return data_by_range

# File pattern to match all .npy files
file_pattern = 'Supplier/Supplier/Sup-*.npy'

# Index ranges of interest
index_ranges = {
    'Range 1 [0, 9]': (0, 9),
    'Range 2 [10, 146]': (10, 146),
    'Range 3 [147, 583]': (147, 583),
    'Range 4 [584, 5000]': (584, 5000)
}

# Read the data from the .npy files at the specified indices
data_by_range = read_data_at_indices(file_pattern, index_ranges)

# Plot the histograms
plt.figure(figsize=(16, 6))

# Use different colors for each histogram
colors = ['blue', 'green', 'red', 'purple']

# Plot each histogram
for i, (range_key, data) in enumerate(data_by_range.items()):
    plt.hist(data, bins=50, alpha=0.6, color=colors[i], label=range_key, density=True)

# Set the labels and title
plt.xlabel('Data Values', fontsize=14)
plt.ylabel('Density', fontsize=14)
plt.title('Histograms of Data Ranges', fontsize=16)

# Add a legend
plt.legend()

# Show the plot
plt.show()
