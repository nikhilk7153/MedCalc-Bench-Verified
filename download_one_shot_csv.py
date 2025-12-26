#!/usr/bin/env python3
"""
Script to download the one_shot split from HuggingFace and save as CSV
"""
from datasets import load_dataset
import pandas as pd

REPO_ID = "nsk7153/MedCalc-Bench-Verified"

print(f"Loading one_shot split from {REPO_ID}...")
dataset = load_dataset(REPO_ID, split="one_shot")

print(f"Loaded {len(dataset)} rows")

# Convert to pandas DataFrame
df = dataset.to_pandas()

# Save to CSV
output_file = "datasets/one_shot_data.csv"
df.to_csv(output_file, index=False)

print(f"Saved {len(df)} rows to {output_file}")
print(f"Columns: {list(df.columns)}")

