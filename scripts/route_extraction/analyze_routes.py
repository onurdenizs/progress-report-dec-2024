"""
analyze_routes.py

Reads the GTFS routes.txt file and performs basic inspection and cleaning.
Saves a cleaned version with useful columns for simulation planning.

Author: Onur Deniz (PhD Railway Engineering)
"""

import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# === File paths ===
RAW_FILE = Path("data/raw/swiss/gtfs_ftp_2025/routes.txt")
CLEANED_FILE = Path("data/processed/routes/cleaned_routes_summary.csv")
CLEANED_FILE.parent.mkdir(parents=True, exist_ok=True)

def main():
    logging.info("🚀 Reading GTFS routes.txt...")
    df = pd.read_csv(RAW_FILE)

    logging.info("✅ Loaded %d rows", len(df))
    logging.info("📌 Columns: %s", ", ".join(df.columns))

    logging.info("🔍 Sample rows:")
    print(df.head(10).to_string(index=False))

    # Save a summary for reference
    logging.info("💾 Saving cleaned summary...")
    summary = df.groupby(['route_type', 'route_desc']).agg({
        'route_id': 'count',
        'route_short_name': lambda x: ', '.join(sorted(set(x.dropna().astype(str))))
    }).rename(columns={'route_id': 'num_routes'})
    summary.to_csv(CLEANED_FILE)

    logging.info(f"✅ Saved cleaned route summary to {CLEANED_FILE.resolve()}")

if __name__ == "__main__":
    main()

