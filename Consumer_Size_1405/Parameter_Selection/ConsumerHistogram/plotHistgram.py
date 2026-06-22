import numpy as np
import matplotlib.pyplot as plt

# Function to load and process data for plotting
def load_data_for_plot(file_dict):
    data_by_range = {}
    for label, filename in file_dict.items():
        data = np.load(filename)
        data_by_range[label] = data
    return data_by_range

# Function to map the data values to the custom x-axis
def transform_data(data, original_x, target_x):
    transformed_data = np.interp(data, original_x, target_x)
    return transformed_data

# Function to plot the histograms with custom x-axis
def plot_with_custom_x_axis(data_by_range):
    fig, ax1 = plt.subplots(figsize=(8, 4))

    # Define the positions and labels for the uneven x-axis ticks
    original_x = np.array([30000, 35000, 40000, 60000, 80000, 95000])
    target_x = np.array([0, 2, 4, 6, 8, 10])

    # Colors for each range
    colors = ['green', 'red', 'purple']

    # Transform and plot the data on ax1 (left y-axis)
    for i, (label, data) in enumerate(data_by_range.items()):
        transformed_data = transform_data(data, original_x, target_x)
        ax1.hist(transformed_data, bins=50, alpha=0.6, color=colors[i], density=True, label=label)

    ax1.set_xlabel('Total Pricing Signal of all Consumers', fontsize=18, fontweight='bold')
    ax1.set_ylabel('Density', fontsize=20, fontweight='bold')
    ax1.tick_params(axis='x', labelcolor='black', labelsize=16)
    ax1.tick_params(axis='y', labelcolor='black', labelsize=16)

    # Set the custom ticks and labels for the x-axis
    ax1.set_xticks(target_x)
    ax1.set_xticklabels(original_x, fontsize=16, fontweight='bold')

    # Set the custom ticks and labels for the y-axis
    ax1.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])
    ax1.set_yticklabels([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], fontweight='bold', fontsize=16)
    ax1.set_ylim(0.0, 0.9)  # Adjusted to include up to 0.6

    # Set limits to match the custom x-axis
    ax1.set_xlim([target_x.min(), target_x.max()])

    # Combine all legends into a single box by creating custom legend handles
    custom_lines = [
    plt.Line2D([0], [0], color=colors[0], lw=4),
    plt.Line2D([0], [0], color=colors[1], lw=4),
    plt.Line2D([0], [0], color=colors[2], lw=4)
    ]
    legend_labels = [
    '$\\mathcal{R}_2$: [10, 146]',
    '$\\mathcal{R}_3$: [147, 583]',
    '$\\mathcal{R}_4$: [584, 5000]'
    ]
    # ax1.legend(custom_lines, legend_labels, loc='center', fontsize=16, title='Ranges', prop={'weight': 'bold'})
    ax1.legend(custom_lines, legend_labels, loc='upper right', prop={'size': 16, 'weight': 'bold'})

    plt.tight_layout()  # Ensures a tight layout
    plt.savefig('ConsumerDistribution1.png', dpi=500)
    # plt.show()

# File names of saved data for each range (simplified keys for loading)
file_dict = {
    'R2': 'Range_2_10_146.npy',
    'R3': 'Range_3_147_583.npy',
    'R4': 'Range_4_584_5000.npy'
}

# Load the saved data
data_by_range = load_data_for_plot(file_dict)

# Update labels to match legend keys
data_by_range = {
    '$\\mathcal{R}_2$: [10, 146]': data_by_range['R2'],
    '$\\mathcal{R}_3$: [147, 583]': data_by_range['R3'],
    '$\\mathcal{R}_4$: [584, 5000]': data_by_range['R4']
}

# Plot the histograms with custom x-axis
plot_with_custom_x_axis(data_by_range)
