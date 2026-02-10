import argparse
import hashlib
import math
from pathlib import Path

import pandas as pd


def stable_group_seed(base_seed: int, group_value: str) -> int:
    # Avoid Python's built-in hash() (hash randomization) so sampling is reproducible.
    payload = f"{base_seed}:{group_value}".encode("utf-8")
    digest = hashlib.sha256(payload).digest()
    return int.from_bytes(digest[:4], "little", signed=False)


def sample_stratified(df: pd.DataFrame, group_col: str, fraction: float, seed: int, min_per_group: int) -> pd.DataFrame:
    if group_col not in df.columns:
        raise ValueError(f"Missing group column: {group_col}")
    if not (0 < fraction <= 1):
        raise ValueError("--fraction must be in (0, 1].")
    if min_per_group < 1:
        raise ValueError("--min-per-group must be >= 1.")

    sampled_groups = []
    for group_value, group_df in df.groupby(group_col, sort=False):
        n = len(group_df)
        k = max(min_per_group, math.ceil(n * fraction))
        k = min(k, n)
        rs = stable_group_seed(seed, str(group_value))
        sampled_groups.append(group_df.sample(n=k, random_state=rs))

    sampled = pd.concat(sampled_groups, ignore_index=True)
    if "Row Number" in sampled.columns:
        sampled = sampled.sort_values("Row Number", kind="mergesort").reset_index(drop=True)
    return sampled


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a stratified subsample of test_data.csv per calculator.")
    parser.add_argument("--input", type=str, default="../datasets/test_data.csv", help="Input CSV path.")
    parser.add_argument("--output", type=str, default="../datasets/test_data_25pct_per_calc.csv", help="Output CSV path.")
    parser.add_argument("--group-col", type=str, default="Calculator ID", help="Column to stratify on.")
    parser.add_argument("--fraction", type=float, default=0.25, help="Fraction per group to sample (roughly).")
    parser.add_argument("--seed", type=int, default=4700, help="Deterministic sampling seed.")
    parser.add_argument("--min-per-group", type=int, default=1, help="Minimum rows to keep per group.")
    args = parser.parse_args()

    input_path = (Path(__file__).resolve().parent / args.input).resolve()
    output_path = (Path(__file__).resolve().parent / args.output).resolve()

    df = pd.read_csv(input_path)
    sampled = sample_stratified(df, args.group_col, args.fraction, args.seed, args.min_per_group)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    sampled.to_csv(output_path, index=False)

    # Minimal stats for sanity-checking.
    group_counts = sampled.groupby(args.group_col).size()
    print(
        "Wrote {} rows to {} (groups={}, min_per_group={}, max_per_group={}).".format(
            len(sampled),
            output_path,
            group_counts.shape[0],
            int(group_counts.min()) if not group_counts.empty else 0,
            int(group_counts.max()) if not group_counts.empty else 0,
        )
    )


if __name__ == "__main__":
    main()

