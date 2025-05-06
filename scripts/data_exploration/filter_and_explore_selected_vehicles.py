"""
Filter and analyze merged SBB vehicle data for selected intercity GTFS routes.

This script loads the merged annual formation + rolling stock dataset, filters
it based on GTFS-selected intercity route train numbers, and explores vehicle
types, Vmax, and seating. Outputs a filtered file for further simulation prep.

Author: Onur Deniz
"""

import pandas as pd
import logging
import os
import csv

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Paths (update if needed)
MERGED_FILE = "data/processed/merged_jahresformation_with_vehicles.csv"
GTFS_FILE = "data/processed/routes/selected_intercity_routes.csv"
OUTPUT_FILE = "data/processed/routes/filtered_vehicle_data_for_simulation.csv"

def detect_separator(filepath: str) -> str:
    """Detect CSV separator for a given file using Python's CSV sniffer."""
    with open(filepath, 'r', encoding='utf-8') as f:
        sample = f.read(2048)
        dialect = csv.Sniffer().sniff(sample)
        logging.info(f"📌 Detected separator: '{dialect.delimiter}'")
        return dialect.delimiter

def extract_train_numbers_from_gtfs(df_gtfs: pd.DataFrame) -> list:
    """Extract unique numeric train numbers from GTFS trip_id strings."""
    df_gtfs = df_gtfs.copy()
    df_gtfs["train_number"] = df_gtfs["trip_id"].str.extract(r"(\d+)")
    return df_gtfs["train_number"].dropna().unique().tolist()

def main():
    logging.info("📂 Detecting separator...")
    sep = detect_separator(MERGED_FILE)

    logging.info("📂 Loading merged dataset...")
    df_merged = pd.read_csv(MERGED_FILE, sep=sep, low_memory=False)
    logging.info(f"✅ Loaded merged shape: {df_merged.shape}")

    logging.info("📂 Loading selected intercity GTFS routes...")
    df_gtfs = pd.read_csv(GTFS_FILE)
    logging.info(f"✅ GTFS shape: {df_gtfs.shape}")

    logging.info("🔢 Extracting train numbers from GTFS trip_id...")
    gtfs_train_numbers = extract_train_numbers_from_gtfs(df_gtfs)
    gtfs_train_numbers_clean = set(str(int(tn)) for tn in gtfs_train_numbers if pd.notna(tn))
    logging.info(f"✅ Extracted {len(gtfs_train_numbers_clean)} unique train numbers.")

    logging.info("🔍 Cleaning train number format in merged dataset...")
    if "Train" not in df_merged.columns:
        logging.warning("⚠️ 'Train' column not found in merged dataset.")
        return

    df_merged["Train_clean"] = df_merged["Train"].astype(str).str.extract(r"(\d+)")[0]
    df_merged["Train_clean"] = df_merged["Train_clean"].dropna().astype(str)

    logging.info("📍 Matching GTFS train numbers with merged dataset...")
    df_filtered = df_merged[df_merged["Train_clean"].isin(gtfs_train_numbers_clean)]
    logging.info(f"✅ Filtered subset shape: {df_filtered.shape}")

    if "Rolling stock" not in df_filtered.columns:
        logging.warning("⚠️ 'Rolling stock' column not found in filtered dataset.")

    logging.info("💾 Saving filtered vehicle data...")
    df_filtered.to_csv(OUTPUT_FILE, index=False)
    logging.info("✅ Done.")

if __name__ == "__main__":
    main()
