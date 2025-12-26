#!/usr/bin/env python3
"""
Script to verify that Ground Truth Answer in one_shot_data.csv matches 
the answer in one_shot_finalized_explanation.json for each Calculator ID
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

print(f"\nComparing {len(df)} rows...\n")

mismatches = []
matches = 0

# Compare each row
for idx, row in df.iterrows():
    calc_id = str(row['Calculator ID'])
    csv_answer = row['Ground Truth Answer']
    
    # Get the answer from JSON
    if calc_id not in json_data:
        print(f"  Warning: Calculator ID {calc_id} not found in JSON file")
        continue
    
    json_entry = json_data[calc_id]
    json_answer = json_entry.get('Response', {}).get('answer')
    
    # Compare the answers
    # Handle different types (int, float, string, list)
    csv_answer_clean = csv_answer
    json_answer_clean = json_answer
    
    # Convert to comparable format
    if pd.isna(csv_answer) or csv_answer == '':
        csv_answer_clean = None
    else:
        # Handle list/tuple format for Calculator ID 69
        if isinstance(json_answer, list):
            # JSON has a list, CSV should have tuple string representation
            # Convert JSON list to tuple string for comparison
            json_answer_clean = str(tuple(json_answer))
            csv_answer_clean = str(csv_answer)
        else:
            # Try to convert to number if possible
            try:
                if isinstance(csv_answer, str):
                    # Try float first (handles decimals)
                    csv_answer_clean = float(csv_answer)
                    # If it's a whole number, convert to int for comparison
                    if csv_answer_clean.is_integer():
                        csv_answer_clean = int(csv_answer_clean)
                else:
                    csv_answer_clean = csv_answer
            except (ValueError, TypeError):
                csv_answer_clean = str(csv_answer)
            # Also convert JSON to same format
            if isinstance(json_answer, (int, float)):
                json_answer_clean = json_answer
            else:
                json_answer_clean = str(json_answer)
    
    # Compare
    if csv_answer_clean != json_answer_clean:
        mismatches.append({
            'Calculator ID': calc_id,
            'CSV Answer': csv_answer,
            'JSON Answer': json_answer,
            'Row Number': row['Row Number']
        })
        print(f"  ❌ Mismatch for Calculator ID {calc_id} (Row {row['Row Number']}):")
        print(f"     CSV:  {csv_answer} (type: {type(csv_answer)})")
        print(f"     JSON: {json_answer} (type: {type(json_answer)})")
    else:
        matches += 1

print(f"\n{'='*60}")
print(f"Summary:")
print(f"  Matches: {matches}")
print(f"  Mismatches: {len(mismatches)}")
print(f"{'='*60}")

if mismatches:
    print("\nMismatches found:")
    for mismatch in mismatches:
        print(f"  Calculator ID {mismatch['Calculator ID']}: CSV={mismatch['CSV Answer']}, JSON={mismatch['JSON Answer']}")
    exit(1)
else:
    print("\n✅ All ground truth answers match!")
    exit(0)

