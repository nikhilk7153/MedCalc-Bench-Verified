#!/usr/bin/env python3
"""
Script to fill Category, Output Type, Note ID, and Note Type in one_shot_data.csv
using the first instance from test_data.csv for each Calculator ID
"""
import pandas as pd

# Read both CSV files
print("Reading one_shot_data.csv...")
one_shot_df = pd.read_csv("datasets/one_shot_data.csv")

print("Reading test_data.csv...")
test_df = pd.read_csv("datasets/test_data.csv")

print(f"One-shot data: {len(one_shot_df)} rows")
print(f"Test data: {len(test_df)} rows")

# Convert metadata columns to object type to avoid dtype warnings
for col in ['Category', 'Output Type', 'Note ID', 'Note Type']:
    one_shot_df[col] = one_shot_df[col].astype('object')

# Get the first instance for each Calculator ID from test_data.csv
print("\nFinding first instance for each Calculator ID in test_data.csv...")
first_instances = test_df.groupby('Calculator ID').first()

# Fill in the metadata fields for each row in one_shot_df
print("\nFilling metadata fields...")
for idx, row in one_shot_df.iterrows():
    calc_id = row['Calculator ID']
    
    if calc_id in first_instances.index:
        first_instance = first_instances.loc[calc_id]
        one_shot_df.at[idx, 'Category'] = first_instance['Category']
        one_shot_df.at[idx, 'Output Type'] = first_instance['Output Type']
        one_shot_df.at[idx, 'Note ID'] = first_instance['Note ID']
        one_shot_df.at[idx, 'Note Type'] = first_instance['Note Type']
        print(f"  Calculator ID {calc_id}: Filled from test_data.csv")
    else:
        print(f"  Warning: Calculator ID {calc_id} not found in test_data.csv")

# Save the updated CSV
output_file = "datasets/one_shot_data.csv"
one_shot_df.to_csv(output_file, index=False)

print(f"\nSaved updated one_shot_data.csv with {len(one_shot_df)} rows")
print(f"Output file: {output_file}")

