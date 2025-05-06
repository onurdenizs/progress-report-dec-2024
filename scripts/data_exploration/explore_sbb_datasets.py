"""
Explore SBB rolling stock and formation datasets.

This script loads and previews the 'jahresformation.csv' and 'rollmaterial.csv' datasets
from the SBB Open Data platform. These datasets include annual train formations and
detailed information about passenger coaches owned by SBB.

Both files use semicolon (;) as the delimiter.

Author: Onur Deniz
"""

import pandas as pd
import logging
from pathlib import Path

# ────────────────────────────────────────────────────────────────────────────────
# Configuration
# ────────────────────────────────────────────────────────────────────────────────

# Enable logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# File paths
DATA_DIR = Path("data/raw/swiss")
OUTPUT_DIR = Path("data/processed")

JAHRESFORMATION_FILE = DATA_DIR / "jahresformation.csv"
ROLLMATERIAL_FILE = DATA_DIR / "rollmaterial.csv"

PREVIEW_JAHRESFORMATION = OUTPUT_DIR / "debug_jahresformation_preview.csv"
PREVIEW_ROLLMATERIAL = OUTPUT_DIR / "debug_rollmaterial_preview.csv"

# ────────────────────────────────────────────────────────────────────────────────
# Load and Inspect
# ────────────────────────────────────────────────────────────────────────────────

def main():
    logging.info("📂 Loading datasets using semicolon separator...")

    try:
        df_jahres = pd.read_csv(JAHRESFORMATION_FILE, sep=";", encoding="utf-8", low_memory=False)
        df_roll = pd.read_csv(ROLLMATERIAL_FILE, sep=";", encoding="utf-8", low_memory=False)
    except Exception as e:
        logging.error("❌ Failed to read CSV files. Check separators or encoding.")
        raise e

    logging.info(f"✅ Jahresformation shape: {df_jahres.shape}")
    logging.info(f"✅ Rollmaterial shape: {df_roll.shape}")

    logging.info(f"📌 Jahresformation sample columns: {list(df_jahres.columns[:10])}")
    logging.info(f"📌 Rollmaterial sample columns: {list(df_roll.columns[:10])}")

    # Save small previews for external review
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df_jahres.head(10).to_csv(PREVIEW_JAHRESFORMATION, index=False)
    df_roll.head(10).to_csv(PREVIEW_ROLLMATERIAL, index=False)

    logging.info(f"💾 Saved preview: {PREVIEW_JAHRESFORMATION}")
    logging.info(f"💾 Saved preview: {PREVIEW_ROLLMATERIAL}")
    logging.info("✅ Data exploration completed.")


if __name__ == "__main__":
    main()
