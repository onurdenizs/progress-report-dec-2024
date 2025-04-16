"""
filter_selected_intercity_data.py

Filters GTFS stop_times data for a given list of selected inter-city route IDs.
Saves the filtered result to a new file for further simulation steps.

Author: Onur Deniz (2025)
"""

import pandas as pd
import logging
from pathlib import Path

# ------------------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------------------

ENRICHED_FILE = Path("data/processed/routes/cleaned_stop_times_enriched.csv")
OUTPUT_FILE = Path("data/processed/routes/selected_intercity_routes.csv")

# Your selected inter-city route IDs
SELECTED_ROUTE_IDS = [
    "91-4E-Y-j25-1",  # Zürich HB → Genève-Aéroport
    "91-5-A-j25-1",   # Lausanne → Rorschach
    "91-6-H-j25-1",   # Basel SBB → Brig
    "91-5F-Y-j25-1",  # Lugano → Zürich HB
    "91-N-Y-j25-1",   # Chur → Basel Bad Bf
]

# ------------------------------------------------------------------------------
# Logging Setup
# ------------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------

def main():
    logging.info(f"📂 Loading enriched stop_times from {ENRICHED_FILE}")
    df = pd.read_csv(ENRICHED_FILE, low_memory=False)

    logging.info(f"🔍 Filtering for selected route IDs ({len(SELECTED_ROUTE_IDS)})...")
    df_filtered = df[df["route_id"].isin(SELECTED_ROUTE_IDS)].copy()

    logging.info(f"✅ Found {len(df_filtered)} rows for selected inter-city routes")
    logging.info(f"💾 Saving to {OUTPUT_FILE}")
    df_filtered.to_csv(OUTPUT_FILE, index=False)

    logging.info("✅ Done.")

# ------------------------------------------------------------------------------
# Run
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
