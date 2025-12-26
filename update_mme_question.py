#!/usr/bin/env python3
"""
Script to update MME calculator question to include CDC opioid conversions reference
"""
import json
import pandas as pd

# The new question text
old_question = "Based on the number of doses per day and the quantity of different doses, what is the patient's daily Morphine Miligram Equivalents (MME)?"
new_question = "Based on the number of doses per day and the quantity of different doses, what is the patient's daily Morphine Miligram Equivalents (MME)? You should use the conversions from the CDC Clinical Practice Guideline for Prescribing Opioids for Pain — United States, 2022."

print("Updating MME calculator question in all files...\n")

# 1. Update name_to_python.json
print("1. Updating name_to_python.json...")
with open("calculator_implementations/name_to_python.json", "r") as f:
    name_to_python = json.load(f)

if "49" in name_to_python:
    name_to_python["49"]["Question"] = new_question
    name_to_python["49"]["question"] = new_question
    with open("calculator_implementations/name_to_python.json", "w") as f:
        json.dump(name_to_python, f, indent=4, ensure_ascii=False)
    print("   ✅ Updated name_to_python.json")
else:
    print("   ⚠️  Calculator ID 49 not found in name_to_python.json")

# 2. Update test_data.csv
print("\n2. Updating test_data.csv...")
test_df = pd.read_csv("datasets/test_data.csv")
test_mask = test_df['Calculator ID'] == 49
test_count = test_mask.sum()
if test_count > 0:
    test_df.loc[test_mask, 'Question'] = new_question
    test_df.to_csv("datasets/test_data.csv", index=False)
    print(f"   ✅ Updated {test_count} rows in test_data.csv")
else:
    print("   ⚠️  No Calculator ID 49 found in test_data.csv")

# 3. Update train_data.csv
print("\n3. Updating train_data.csv...")
train_df = pd.read_csv("datasets/train_data.csv")
train_mask = train_df['Calculator ID'] == 49
train_count = train_mask.sum()
if train_count > 0:
    train_df.loc[train_mask, 'Question'] = new_question
    train_df.to_csv("datasets/train_data.csv", index=False)
    print(f"   ✅ Updated {train_count} rows in train_data.csv")
else:
    print("   ⚠️  No Calculator ID 49 found in train_data.csv")

# 4. Update one_shot_data.csv
print("\n4. Updating one_shot_data.csv...")
one_shot_df = pd.read_csv("datasets/one_shot_data.csv")
one_shot_mask = one_shot_df['Calculator ID'] == 49
one_shot_count = one_shot_mask.sum()
if one_shot_count > 0:
    one_shot_df.loc[one_shot_mask, 'Question'] = new_question
    one_shot_df.to_csv("datasets/one_shot_data.csv", index=False)
    print(f"   ✅ Updated {one_shot_count} rows in one_shot_data.csv")
else:
    print("   ⚠️  No Calculator ID 49 found in one_shot_data.csv")

print(f"\n✅ All files updated!")
print(f"\nNew question: {new_question}")

