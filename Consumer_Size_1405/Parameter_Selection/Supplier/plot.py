import numpy as np
import matplotlib.pyplot as plt
import glob

# Function to read all .npy files and calculate the mean and standard deviation
def read_and_process_files(file_pattern):
    all_data = []
    for filename in glob.glob(file_pattern):
        data = np.load(filename)
        all_data.append(data)
    all_data = np.array(all_data)
    mean_data = np.mean(all_data, axis=0)
    std_data = np.std(all_data, axis=0)
    return all_data, mean_data, std_data

# Function to find the indices of the smallest and largest values for each digit length
def find_min_max_indices(values):
    digit_length_to_indices = {}
    for i, value in enumerate(values):
        if not np.isnan(value):
            digit_length = len(str(int(value)))
            if digit_length not in digit_length_to_indices:
                digit_length_to_indices[digit_length] = {'min': (i, value), 'max': (i, value)}
            else:
                if value < digit_length_to_indices[digit_length]['min'][1]:
                    digit_length_to_indices[digit_length]['min'] = (i, value)
                if value > digit_length_to_indices[digit_length]['max'][1]:
                    digit_length_to_indices[digit_length]['max'] = (i, value)
    return digit_length_to_indices

# File pattern to match all .npy files
file_pattern = 'Supplier/Supplier/Sup-*.npy'

# Read and process the files
all_data, mean_data, std_data = read_and_process_files(file_pattern)

# Ensure mean_data and std_data are arrays and not single values
mean_data = np.atleast_1d(mean_data)
std_data = np.atleast_1d(std_data)

# Check if the arrays are non-empty
if mean_data.size == 0 or std_data.size == 0:
    raise ValueError("The mean or standard deviation arrays are empty. Check the input files and data processing.")

# Debug print to check the contents of mean_data and std_data
print(f"Mean data: {mean_data[:10]}")
print(f"Standard deviation data: {std_data[:10]}")

# Find min and max indices for mean and standard deviation
mean_min_max_indices = find_min_max_indices(mean_data)
std_min_max_indices_upper = find_min_max_indices(mean_data + std_data)
std_min_max_indices_lower = find_min_max_indices(mean_data - std_data)

# Plot the mean data with standard deviation bounds
x = np.arange(len(mean_data))
plt.figure(figsize=(8, 8))
plt.plot(x, mean_data, label='Mean of all the simulations', color='blue')
plt.fill_between(x, mean_data - std_data, mean_data + std_data, color='blue', alpha=0.2, label='Standard Deviation')

# Increase number of x-ticks and y-ticks to 10
plt.xticks([0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000], fontsize=14, rotation=45)
plt.yticks([0, 5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000], fontsize=14)

# Increase the font size of x and y axis labels
plt.xlabel('Sampling Windows', fontsize=16)
plt.ylabel('Total Pricing Signal', fontsize=16)

# Create dictionary to store the legend information
digit_info = {}

# Collect the legend information
for digit_length in sorted(mean_min_max_indices.keys()):
    mean_min = mean_min_max_indices[digit_length]['min']
    mean_max = mean_min_max_indices[digit_length]['max']
    lower_min = std_min_max_indices_lower[digit_length]['min']
    lower_max = std_min_max_indices_lower[digit_length]['max']
    upper_min = std_min_max_indices_upper[digit_length]['min']
    upper_max = std_min_max_indices_upper[digit_length]['max']

    digit_info[digit_length] = {
        'lower': {'min': lower_min, 'max': lower_max},
        'mean': {'min': mean_min, 'max': mean_max},
        'upper': {'min': upper_min, 'max': upper_max}
    }

# Prepare legend entries
legend_entries = []
for digit, values in digit_info.items():
    entry = (f"Digit {digit}:\n"
             f"Lower Bound => Value: [{values['lower']['min'][1]:.2f}, {values['lower']['max'][1]:.2f}], "
             f"Iteration: [{values['lower']['min'][0]}, {values['lower']['max'][0]}]\n"
             f"Mean Bound  => Value: [{values['mean']['min'][1]:.2f}, {values['mean']['max'][1]:.2f}], "
             f"Iteration: [{values['mean']['min'][0]}, {values['mean']['max'][0]}]\n"
             f"Upper Bound => Value: [{values['upper']['min'][1]:.2f}, {values['upper']['max'][1]:.2f}], "
             f"Iteration: [{values['upper']['min'][0]}, {values['upper']['max'][0]}]\n")
    legend_entries.append(entry)

plt.show()
