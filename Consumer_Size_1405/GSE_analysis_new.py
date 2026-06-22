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
GSE_RE = re.compile(
    r"^\s*GSE\s+plain=([+-]?[0-9.]+e[+-]\d+)\s+privprice=([+-]?[0-9.]+e[+-]\d+)\s*$",
    re.IGNORECASE,
)


def parse_gse_lists(
    log_path: Path,
    max_iterations: int | None = 673,
) -> Tuple[List[float], List[float], List[float], List[float], List[int], List[dict]]:
    """
    Parse the log and return:
      - gse_plain:       [plain_t1, plain_t2, ...]
      - gse_priv:        [priv_t1,  priv_t2,  ...]
      - gse_orig_over_priv: [plain/priv per iteration]
      - gse_priv_over_orig: [priv/plain per iteration]
      - iteration_numbers
      - raw_rows
    """
    lines = log_path.read_text(encoding="utf-8", errors="replace").splitlines()

    gse_plain: List[float] = []
    gse_priv: List[float] = []
    gse_orig_over_priv: List[float] = []
    gse_priv_over_orig: List[float] = []
    iteration_numbers: List[int] = []
    raw_rows: List[dict] = []

    current_iter: int | None = None

    for line in lines:
        m_iter = ITER_RE.match(line.strip())
        if m_iter:
            current_iter = int(m_iter.group(1))
            continue

        m_gse = GSE_RE.match(line.strip())
        if m_gse:
            if current_iter is None:
                raise ValueError("Found GSE line before an iteration header.")

            plain = float(m_gse.group(1))
            priv = float(m_gse.group(2))

            orig_over_priv = (plain / priv) if priv != 0.0 else math.inf
            priv_over_orig = (priv / plain) if plain != 0.0 else math.inf

            gse_plain.append(plain)
            gse_priv.append(priv)
            gse_orig_over_priv.append(orig_over_priv)
            gse_priv_over_orig.append(priv_over_orig)
            iteration_numbers.append(current_iter)

            raw_rows.append(
                {
                    "iteration": current_iter,
                    "plain": plain,
                    "privprice": priv,
                    "orig_over_priv": orig_over_priv,
                    "priv_over_orig": priv_over_orig,
                    "abs_1_minus_orig_over_priv": abs(1.0 - orig_over_priv),
                    "abs_1_minus_priv_over_orig": abs(1.0 - priv_over_orig),
                }
            )

            if max_iterations is not None and len(iteration_numbers) >= max_iterations:
                break

    return (
        gse_plain,
        gse_priv,
        gse_orig_over_priv,
        gse_priv_over_orig,
        iteration_numbers,
        raw_rows,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Parse GSE plain/privprice values and ratios from a PrivPrice detailed log."
    )
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
        help="Maximum number of RTP iterations to parse",
    )
    parser.add_argument(
        "--json-out",
        type=Path,
        default=Path("gse_lists.json"),
        help="Output JSON file",
    )
    parser.add_argument(
        "--npy-out",
        type=Path,
        default=Path("gse_lists.npy"),
        help="Output .npy file with shape (4, T)",
    )
    args = parser.parse_args()

    (
        gse_plain,
        gse_priv,
        gse_orig_over_priv,
        gse_priv_over_orig,
        iteration_numbers,
        raw_rows,
    ) = parse_gse_lists(
        args.log_file,
        max_iterations=args.max_iterations,
    )

    matrix = np.array(
        [
            gse_plain,
            gse_priv,
            gse_orig_over_priv,
            gse_priv_over_orig,
        ],
        dtype=np.float64,
    )

    payload = {
        "num_iterations": len(iteration_numbers),
        "iterations": iteration_numbers,
        "gse_plain": gse_plain,
        "gse_privprice": gse_priv,
        "gse_orig_over_priv": gse_orig_over_priv,
        "gse_priv_over_orig": gse_priv_over_orig,
        "raw_rows": raw_rows,
    }

    args.json_out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    np.save(args.npy_out, matrix)

    print(f"Parsed {len(iteration_numbers)} RTP iterations from: {args.log_file}")
    print(f"JSON written to: {args.json_out}")
    print(f"NumPy matrix written to: {args.npy_out} with shape {matrix.shape}")
    print()

    print("gse_plain = ", gse_plain)
    print()
    print("gse_privprice = ", gse_priv)
    print()
    print("gse_orig_over_priv = ", gse_orig_over_priv)
    print()
    print("gse_priv_over_orig = ", gse_priv_over_orig)


if __name__ == "__main__":
    main()