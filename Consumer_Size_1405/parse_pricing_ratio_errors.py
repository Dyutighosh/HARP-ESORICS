#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

ITER_RE = re.compile(r"^RTP iteration\s+(\d+)\s*$")
ROW_RE = re.compile(
    r"^\s*C\[(\d{2})\]\s+orig=([+-]?[0-9.]+e[+-]\d+)\s+priv=([+-]?[0-9.]+e[+-]\d+)\s+priv/orig=([+-]?[0-9.]+e[+-]\d+)\s+rel_err=([+-]?[0-9.]+e[+-]\d+)%\s*$",
    re.IGNORECASE,
)
HEADER = "First 10 consumer next-price comparison [idx, original, privprice, priv/original, rel_err%]:"


def parse_consumer_error_lists(
    log_path: Path,
    max_iterations: int | None = 3000,
    metric: str = "orig_over_priv",
) -> Tuple[Dict[int, List[float]], List[int], Dict[int, List[dict]]]:

    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()

    error_lists: Dict[int, List[float]] = {i: [] for i in range(10)}
    raw_rows: Dict[int, List[dict]] = {i: [] for i in range(10)}
    iteration_numbers: List[int] = []

    current_iter: int | None = None
    i = 0
    while i < len(lines):
        line = lines[i]

        m_iter = ITER_RE.match(line.strip())
        if m_iter:
            current_iter = int(m_iter.group(1))
            i += 1
            continue

        if HEADER in line:
            if current_iter is None:
                raise ValueError(
                    f"Found consumer comparison block before an iteration header at line {i+1}."
                )

            block_rows = 0
            for j in range(1, 11):
                if i + j >= len(lines):
                    break
                m_row = ROW_RE.match(lines[i + j])
                if not m_row:
                    break

                consumer_idx = int(m_row.group(1))
                orig = float(m_row.group(2))
                priv = float(m_row.group(3))
                priv_over_orig = float(m_row.group(4))
                rel_err_percent = float(m_row.group(5))

                if metric == "orig_over_priv":
                    error = abs(1.0 - (orig / priv)) if priv != 0.0 else math.inf
                elif metric == "priv_over_orig":
                    error = abs(1.0 - priv_over_orig)
                elif metric == "logged_rel_percent":
                    error = rel_err_percent / 100.0
                else:
                    raise ValueError(f"Unknown metric: {metric}")

                error_lists[consumer_idx].append(error)
                raw_rows[consumer_idx].append(
                    {
                        "iteration": current_iter,
                        "orig": orig,
                        "priv": priv,
                        "priv_over_orig": priv_over_orig,
                        "logged_rel_err_percent": rel_err_percent,
                        "requested_error": error,
                    }
                )
                block_rows += 1

            if block_rows == 10:
                iteration_numbers.append(current_iter)
                if max_iterations is not None and len(iteration_numbers) >= max_iterations:
                    break
            i += max(1, block_rows)
            continue

        i += 1

    return error_lists, iteration_numbers, raw_rows


def to_matrix(error_lists: Dict[int, List[float]]) -> np.ndarray:
    lengths = {len(v) for v in error_lists.values()}
    if len(lengths) != 1:
        raise ValueError(f"Consumers do not all have the same number of parsed iterations: {lengths}")
    return np.array([error_lists[i] for i in range(10)], dtype=np.float64)


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse first-10-consumer price-ratio error lists from a PrivPrice detailed log.")
    parser.add_argument(
        "log_file",
        type=Path,
        nargs="?",
        default=Path("privprice_detailed_protocol.log"),
        help="Path to privprice_detailed_protocol.log",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=3000,
        help="Maximum number of RTP iterations to parse (default: 300)",
    )
    parser.add_argument(
        "--metric",
        choices=["orig_over_priv", "priv_over_orig", "logged_rel_percent"],
        default="orig_over_priv",
        help=(
            "Error metric to store: "
            "orig_over_priv = abs(1 - original/privprice) [default], "
            "priv_over_orig = abs(1 - privprice/original), "
            "logged_rel_percent = rel_err%% column converted to unitless fraction"
        ),
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=Path("consumer_pricing_ratio_error_lists.json"),
        help="Output JSON file",
    )
    parser.add_argument(
        "--npy-out",
        type=Path,
        default=Path("consumer_pricing_ratio_error_lists.npy"),
        help="Output .npy matrix file",
    )
    args = parser.parse_args()

    error_lists, iteration_numbers, raw_rows = parse_consumer_error_lists(
        args.log_file,
        max_iterations=args.max_iterations,
        metric=args.metric,
    )

    matrix = to_matrix(error_lists)

    payload = {
        "metric": args.metric,
        "num_consumers": 10,
        "num_iterations": len(iteration_numbers),
        "iterations": iteration_numbers,
        "error_lists": {f"consumer_{i+1}": error_lists[i] for i in range(10)},
        "raw_rows": {f"consumer_{i+1}": raw_rows[i] for i in range(10)},
    }
    args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    np.save(args.npy_out, matrix)

    print(f"Parsed {len(iteration_numbers)} RTP iterations from: {args.log_file}")
    print(f"Metric: {args.metric}")
    print(f"JSON written to: {args.json_out}")
    print(f"NumPy matrix written to: {args.npy_out} with shape {matrix.shape}")
    print()
    print("Python lists for the first 10 consumers:")
    for idx in range(10):
        print(f"consumer_{idx+1} = {error_lists[idx]}")


if __name__ == "__main__":
    main()
