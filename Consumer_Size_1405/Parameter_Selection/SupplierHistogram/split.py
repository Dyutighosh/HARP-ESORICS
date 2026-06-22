# split_npy.py
import os, math, json, pathlib
import numpy as np

def split_npy(path, target_mb=90):
    p = pathlib.Path(path)
    arr = np.load(p, allow_pickle=False)
    nbytes = arr.nbytes
    parts = max(1, math.ceil(nbytes / (target_mb * 1024 * 1024)))
    if parts == 1:
        print("Already under target size.")
        return [str(p)]

    out_dir = p.parent / (p.stem + ".parts")
    out_dir.mkdir(parents=True, exist_ok=True)

    # split along the first axis
    idxs = np.linspace(0, arr.shape[0], parts + 1, dtype=int)
    out_files = []
    for i in range(parts):
        sl = slice(idxs[i], idxs[i+1])
        chunk = arr[sl]
        out_file = out_dir / f"{p.stem}.part{i+1:02d}.npy"
        np.save(out_file, chunk)
        out_files.append(out_file.name)
        print("Wrote", out_file)

    # write a tiny manifest (handy for loading)
    (out_dir / "manifest.json").write_text(json.dumps({
        "original": str(p.name), "shape": arr.shape, "dtype": str(arr.dtype),
        "parts": out_files
    }, indent=2))
    return [str(out_dir / f) for f in out_files]

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python split_npy.py PATH/Range_4_584_5000.npy")
        sys.exit(1)
    split_npy(sys.argv[1])
