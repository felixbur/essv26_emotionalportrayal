#!/usr/bin/env python
"""Merge all_predicted.csv and segmented.csv column-wise."""

import pandas as pd

# Read both CSV files
print("Reading all_predicted.csv...")
all_predicted = pd.read_csv("segmented_linguistic-labels.csv")

print("Reading segmented.csv...")
segmented = pd.read_csv("segmented_acoustic-labels.csv")

print(f"all_predicted shape: {all_predicted.shape}")
print(f"segmented shape: {segmented.shape}")

# Identify common columns to use as merge keys
common_cols = [
    "file",
    "start",
    "end",
    "speaker",
    "gender",
    "age",
    "birth_year",
    "duration",
    "emotion",
    "text",
]

# Get unique columns from each dataframe
all_predicted_unique = [col for col in all_predicted.columns if col not in common_cols]
segmented_unique = [col for col in segmented.columns if col not in common_cols]

print(f"\nUnique columns from all_predicted: {all_predicted_unique}")
print(f"Unique columns from segmented: {segmented_unique}")

# Merge on the common columns
# Using inner join to keep only matching rows
merged = pd.merge(
    all_predicted,
    segmented[common_cols + segmented_unique],
    on=common_cols,
    how="inner",
)

print(f"\nMerged shape: {merged.shape}")
print(f"Merged columns: {list(merged.columns)}")

# Save the merged dataframe
output_file = "segmented_combined.csv"
merged.to_csv(output_file, index=False)
print(f"\nSaved merged dataframe to {output_file}")
