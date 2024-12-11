"""
french_lines_preprocessing.py

Script to preprocess French railway line data.
"""

import pandas as pd
import os

# File paths
input_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/raw/french/caracteristique_des_voies/caracteristique_des_voies.csv"
output_dir = "D:/PhD/codingPractices/progress-report-dec-2024/data/processed/french"
output_file = os.path.join(output_dir, "french_lines.csv")

try:
    print("Loading dataset...")
    # Load dataset with correct delimiter
    df = pd.read_csv(input_file, sep=";", dtype={"CODE_LIGNE": str})

    print("Dataset loaded successfully!")

    print("Cleaning column names...")
    # Standardize column names
    df.columns = df.columns.str.strip().str.replace('\ufeff', '')
    df.columns = df.columns.str.upper()
    print("Cleaned column names:", df.columns.tolist())

    print("Processing unique lines...")
    # Select relevant columns
    if 'CODE_LIGNE' not in df.columns or 'LIB_LIGNE' not in df.columns:
        raise KeyError("Required columns ('CODE_LIGNE', 'LIB_LIGNE') not found in dataset.")

    unique_lines = df[['CODE_LIGNE', 'LIB_LIGNE']].drop_duplicates()

    # Ensure CODE_LIGNE is a string and pad with leading zeros
    unique_lines['CODE_LIGNE'] = unique_lines['CODE_LIGNE'].astype(str).apply(lambda x: x.zfill(6))

    # Extract origin and destination from LIB_LIGNE
    def extract_origin_destination(lib_ligne):
        if "Ligne de " in lib_ligne and " à " in lib_ligne:
            parts = lib_ligne.replace("Ligne de ", "").split(" à ", 1)
            return parts[0].strip(), parts[1].strip()
        return None, None

    unique_lines[['origin', 'destination']] = unique_lines['LIB_LIGNE'].apply(
        lambda x: pd.Series(extract_origin_destination(x))
    )

    # Sort by line code in ascending order
    unique_lines = unique_lines.sort_values(by="CODE_LIGNE")
    print(f"{len(unique_lines)} unique lines processed.")

    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    unique_lines.to_csv(output_file, index=False)
    print(f"Processed data saved to: {output_file}")

except FileNotFoundError as fnfe:
    print(f"File not found: {fnfe}")
except KeyError as ke:
    print(f"Missing column: {ke}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
