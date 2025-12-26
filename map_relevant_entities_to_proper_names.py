#!/usr/bin/env python3
"""
Script to map Relevant Entities from Python names to proper names using name_to_python.json
"""
import json
import pandas as pd

# Load the name to Python mapping
print("Loading name_to_python.json...")
with open("calculator_implementations/name_to_python.json", "r") as f:
    name_to_python = json.load(f)

# Keys to skip when creating the reverse mapping
skip_keys = {"file path", "explanation function", "calculator name", "type", "question"}

# Create reverse mappings for each calculator ID (Python name -> Proper name)
print("Creating reverse mappings...")
python_to_proper = {}
for calc_id, mappings in name_to_python.items():
    reverse_map = {}
    for proper_name, python_name in mappings.items():
        if proper_name not in skip_keys:
            reverse_map[python_name] = proper_name
    python_to_proper[calc_id] = reverse_map

# Read the one_shot_data.csv
print("Reading one_shot_data.csv...")
df = pd.read_csv("datasets/one_shot_data.csv")

print(f"Processing {len(df)} rows...")

# Process each row
updated_count = 0
for idx, row in df.iterrows():
    calc_id = str(row['Calculator ID'])
    relevant_entities_str = row['Relevant Entities']
    
    if pd.isna(relevant_entities_str) or relevant_entities_str == '':
        continue
    
    try:
        # Parse the JSON string
        if isinstance(relevant_entities_str, str):
            relevant_entities = json.loads(relevant_entities_str)
        else:
            relevant_entities = relevant_entities_str
        
        # Get the reverse mapping for this calculator ID
        if calc_id not in python_to_proper:
            print(f"  Warning: Calculator ID {calc_id} not found in name_to_python.json")
            continue
        
        reverse_map = python_to_proper[calc_id]
        
        # Create new dictionary with proper names
        new_relevant_entities = {}
        for key, value in relevant_entities.items():
            # Map Python name to proper name
            proper_name = reverse_map.get(key, key)  # Use original if not found
            new_relevant_entities[proper_name] = value
        
        # Update the row
        df.at[idx, 'Relevant Entities'] = json.dumps(new_relevant_entities, ensure_ascii=False)
        updated_count += 1
        
    except json.JSONDecodeError as e:
        print(f"  Warning: Row {idx+1} (Calculator ID {calc_id}) - JSON decode error: {e}")
        continue
    except Exception as e:
        print(f"  Warning: Row {idx+1} (Calculator ID {calc_id}) - Error: {e}")
        continue

print(f"\nUpdated {updated_count} rows")

# Save the updated CSV
output_file = "datasets/one_shot_data.csv"
df.to_csv(output_file, index=False)

print(f"Saved updated one_shot_data.csv to {output_file}")

