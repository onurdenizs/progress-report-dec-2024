"""
analyze_sbb_vehicle_and_formation.py

This script loads and explores the SBB "jahresformation" and "rollmaterial" datasets,
performs basic cleaning, and investigates links between vehicle types and formation entries.

Author: Onur Deniz
"""

import pandas as pd
import logging
import os

# ────────────────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────────────────
DATA_DIR = "data/raw/swiss"
PROCESSED_DIR = "data/processed/debug"

JAHRESFORMATION_PATH = os.path.join(DATA_DIR, "jahresformation.csv")
ROLLMATERIAL_PATH = os.path.join(DATA_DIR, "rollmaterial.csv")

os.makedirs(PROCESSED_DIR, exist_ok=True)

# ────────────────────────────────────────────────────────────────────────────────
# Setup logging
# ────────────────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ────────────────────────────────────────────────────────────────────────────────
# Load Data
# ────────────────────────────────────────────────────────────────────────────────
def load_data():
    logging.info("📂 Loading datasets using semicolon separator...")
    df_jahres = pd.read_csv(JAHRESFORMATION_PATH, sep=";", low_memory=False)
    df_roll = pd.read_csv(ROLLMATERIAL_PATH, sep=";", low_memory=False)
    
    logging.info(f"✅ Jahresformation shape: {df_jahres.shape}")
    logging.info(f"✅ Rollmaterial shape: {df_roll.shape}")
    return df_jahres, df_roll

# ────────────────────────────────────────────────────────────────────────────────
# Analyze Linkage Potential
# ────────────────────────────────────────────────────────────────────────────────
def explore_linkage(df_jahres, df_roll):
    logging.info("🔗 Exploring linkage between 'block_bezeichnung' and 'Vehicle type'...")

    # Clean and inspect keys
    blocks_in_jahres = df_jahres["Block designation"].dropna().unique()
    types_in_roll = df_roll["Vehicle type"].dropna().unique()

    overlap = set(blocks_in_jahres) & set(types_in_roll)
    logging.info(f"🔍 Unique block_bezeichnung in jahresformation: {len(blocks_in_jahres)}")
    logging.info(f"🔍 Unique vehicle types in rollmaterial: {len(types_in_roll)}")
    logging.info(f"🔁 Overlapping types (used for linking): {len(overlap)}")

    # Save a CSV for manual inspection
    linkage_sample = pd.DataFrame(sorted(list(overlap)), columns=["shared_vehicle_type"])
    linkage_sample.to_csv(os.path.join(PROCESSED_DIR, "shared_vehicle_types.csv"), index=False)
    logging.info(f"💾 Saved shared vehicle type list to: {PROCESSED_DIR}/shared_vehicle_types.csv")

# ────────────────────────────────────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────────────────────────────────────
def main():
    df_jahres, df_roll = load_data()
    explore_linkage(df_jahres, df_roll)

if __name__ == "__main__":
    main()
