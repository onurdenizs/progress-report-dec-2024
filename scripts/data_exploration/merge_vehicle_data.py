"""
merge_vehicle_data.py

This script merges the annual train formation dataset (jahresformation) with the
rolling stock equipment information (rollmaterial), using the vehicle type matching
table (rollmaterial-matching) as a bridge. The goal is to enrich the formation data
with detailed vehicle attributes for use in railway simulation and analysis.

Author: Onur Deniz
Date: 2025-04-16
"""

import pandas as pd
import logging
from pathlib import Path

# ----------------------------- Configuration -----------------------------

DATA_DIR = Path("data/raw/swiss")
OUTPUT_DIR = Path("data/processed")

JAHRESFORMATION_FILE = DATA_DIR / "jahresformation.csv"
ROLLMATERIAL_FILE = DATA_DIR / "rollmaterial.csv"
MATCHING_FILE = DATA_DIR / "rollmaterial-matching.csv"

OUTPUT_MERGED_FILE = OUTPUT_DIR / "merged_jahresformation_with_vehicles.csv"

# ----------------------------- Logging Setup -----------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ---------------------------- Main Function ------------------------------

def merge_datasets():
    logging.info("📂 Loading datasets using semicolon separator...")

    # Load datasets
    df_jahres = pd.read_csv(JAHRESFORMATION_FILE, sep=";", low_memory=False)
    df_roll = pd.read_csv(ROLLMATERIAL_FILE, sep=";", low_memory=False)
    df_match = pd.read_csv(MATCHING_FILE, sep=";", low_memory=False)

    logging.info(f"✅ Jahresformation: {df_jahres.shape}")
    logging.info(f"✅ Rollmaterial: {df_roll.shape}")
    logging.info(f"✅ Matching table: {df_match.shape}")

    # Rename matching columns for consistency
    df_match.rename(columns={
        "Train scheduling": "zugplanung",
        "Rolling stock": "rollmaterial"
    }, inplace=True)

    # ---------------------- Step 1: Merge Jahres + Matching ----------------------

    logging.info("🔗 Linking jahresformation with vehicle types...")
    df_merged = df_jahres.merge(
        df_match,
        how="left",
        left_on="Block designation",  # previously 'block_bezeichnung'
        right_on="zugplanung"
    )

    logging.info(f"✅ After 1st merge: {df_merged.shape}")

    # ---------------------- Step 2: Merge with Rollmaterial ----------------------

    logging.info("🚆 Linking with detailed rolling stock data...")
    df_merged = df_merged.merge(
        df_roll,
        how="left",
        left_on="rollmaterial",
        right_on="Vehicle type"
    )

    logging.info(f"✅ Final merged shape: {df_merged.shape}")

    # ---------------------- Save Output ----------------------

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_merged.to_csv(OUTPUT_MERGED_FILE, index=False)
    logging.info(f"💾 Saved merged dataset to: {OUTPUT_MERGED_FILE}")

# ----------------------------- Entrypoint -------------------------------

if __name__ == "__main__":
    merge_datasets()
