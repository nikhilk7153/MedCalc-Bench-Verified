#!/usr/bin/env python3
"""
Script to fix Ground Truth Answer in one_shot_data.csv to match 
one_shot_finalized_explanation.json
"""
import json
import pandas as pd

# Read the CSV file
print("Reading one_shot_data.csv...")
df = pd.read_csv("datasets/one_shot_data.csv")

# Read the JSON file
print("Reading one_shot_finalized_explanation.json...")
with open("evaluation/one_shot_finalized_explanation.json", "r") as f:
    json_data = json.load(f)

print(f"\nFixing {len(df)} rows...\n")

fixed_count = 0

# Fix each row
for idx, row in df.iterrows():
    calc_id = str(row['Calculator ID'])
    
    # Get the answer from JSON
    if calc_id not in json_data:
        print(f"  Warning: Calculator ID {calc_id} not found in JSON file")
        continue
    
    json_entry = json_data[calc_id]
    json_answer = json_entry.get('Response', {}).get('answer')
    
    # Convert JSON answer to string format (matching CSV format)
    if json_answer is None:
        csv_answer = None
    elif isinstance(json_answer, list):
        # For lists (like Calculator ID 69), convert to tuple string representation
        csv_answer = str(tuple(json_answer))
    else:
        csv_answer = str(json_answer)
    
    # Update the CSV
    current_answer = row['Ground Truth Answer']
    if str(current_answer) != str(csv_answer):
        print(f"  Fixing Calculator ID {calc_id} (Row {row['Row Number']}):")
        print(f"    Old: {current_answer}")
        print(f"    New: {csv_answer}")
        df.at[idx, 'Ground Truth Answer'] = csv_answer
        fixed_count += 1

# Save the updated CSV
if fixed_count > 0:
    output_file = "datasets/one_shot_data.csv"
    df.to_csv(output_file, index=False)
    print(f"\n✅ Fixed {fixed_count} rows and saved to {output_file}")
else:
    print("\n✅ No fixes needed - all answers already match!")

