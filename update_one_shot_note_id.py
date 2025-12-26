#!/usr/bin/env python3
"""
Script to update Note ID in one_shot_data.csv to format: one_shot_{calculator_id}
"""
import pandas as pd

# Read the one_shot_data.csv
print("Reading one_shot_data.csv...")
df = pd.read_csv("datasets/one_shot_data.csv")

print(f"Processing {len(df)} rows...")

# Update Note ID for each row
for idx, row in df.iterrows():
    calc_id = row['Calculator ID']
    df.at[idx, 'Note ID'] = f"one_shot_{calc_id}"

print(f"Updated Note ID for all {len(df)} rows")

# Save the updated CSV
output_file = "datasets/one_shot_data.csv"
df.to_csv(output_file, index=False)

print(f"Saved updated one_shot_data.csv to {output_file}")

