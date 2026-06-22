import os, math, json, pathlib, glob
import numpy as np
import matplotlib.pyplot as plt

# ---------- splitting & loading helpers ----------

def split_npy(path, target_mb=90):
    """
    Split a large .npy into ~target_mb chunks along axis 0.
    Creates a sibling directory '<stem>.parts' with part files and a manifest.json.
    Returns the Path to the parts directory.
    """
    p = pathlib.Path(path)
    out_dir = p.parent / (p.stem + ".parts")
    out_dir.mkdir(parents=True, exist_ok=True)

    # mmap so we don't load the whole thing into RAM at once
    arr = np.load(str(p), allow_pickle=False, mmap_mode='r')
    nbytes = arr.dtype.itemsize * int(np.prod(arr.shape))
    parts = max(1, math.ceil(nbytes / (target_mb * 1024 * 1024)))
    if parts == 1:
        # nothing to do; remove empty dir we might've made
        try:
            out_dir.rmdir()
        except OSError:
            pass
        return p

    idxs = np.linspace(0, arr.shape[0], parts + 1, dtype=int)
    out_files = []
    for i in range(parts):
        sl = slice(idxs[i], idxs[i + 1])
        chunk = np.asarray(arr[sl])  # ensure a real ndarray, not a memmap view
        out_file = out_dir / f"{p.stem}.part{i+1:02d}.npy"
        np.save(str(out_file), chunk)
        out_files.append(out_file.name)
        print(f"Wrote {out_file} shape={chunk.shape}")

    manifest = {
        "original": p.name,
        "shape": tuple(int(x) for x in arr.shape),
        "dtype": str(arr.dtype),
        "parts": out_files,
    }
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return out_dir


def ensure_parts_or_single(path, threshold_mb=95):
    """
    If <stem>.parts exists (with parts), use that.
    Else, if file size > threshold_mb, split; otherwise return the original file.
    Returns either a Path to the .npy file or to the .parts directory.
    """
    p = pathlib.Path(path)
    parts_dir = p.parent / (p.stem + ".parts")
    if parts_dir.exists() and list(parts_dir.glob("*.part*.npy")):
        return parts_dir
    # quick check on the on-disk file size (slightly smaller than arr.nbytes but good enough)
    if p.exists() and p.stat().st_size > threshold_mb * 1024 * 1024:
        return split_npy(p, target_mb=threshold_mb - 5)
    return p


def load_multipart(path_or_dir):
    """
    Load either a single .npy, a directory of parts, or a specific .partXX.npy by concatenating on axis 0.
    """
    p = pathlib.Path(path_or_dir)
    if p.is_dir():
        man = p / "manifest.json"
        if man.exists():
            info = json.loads(man.read_text())
            files = [p / name for name in info["parts"]]
        else:
            files = sorted(p.glob("*.part*.npy"))
        arrays = [np.load(str(f), allow_pickle=False) for f in files]
        return np.concatenate(arrays, axis=0)

    if p.suffix == ".npy" and ".part" in p.stem:
        base = p.stem.split(".part")[0]
        files = sorted(p.parent.glob(base + ".part*.npy"))
        arrays = [np.load(str(f), allow_pickle=False) for f in files]
        return np.concatenate(arrays, axis=0)

    return np.load(str(p), allow_pickle=False)

# ---------- your existing logic (with small tweaks) ----------

# Function to load and process data for plotting
def load_data_for_plot(file_dict):
    data_by_range = {}
    for label, filename in file_dict.items():
        data_by_range[label] = load_multipart(filename)
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
    ax1.set_ylim(0.0, 0.9)

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
    ax1.legend(custom_lines, legend_labels, loc='upper right', prop={'size': 16, 'weight': 'bold'})

    plt.tight_layout()
    plt.savefig('ConsumerDistribution1.png', dpi=500)
    # plt.show()

# ---- configure files (R4 will be auto-split if too large) ----

R4_PATH = 'Range_4_584_5000.npy'  # adjust path if yours lives elsewhere
R4_SOURCE = ensure_parts_or_single(R4_PATH, threshold_mb=95)

file_dict = {
    'R2': 'Range_2_10_146.npy',
    'R3': 'Range_3_147_583.npy',
    'R4': str(R4_SOURCE)  # either '...npy' or the '...parts' directory
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
