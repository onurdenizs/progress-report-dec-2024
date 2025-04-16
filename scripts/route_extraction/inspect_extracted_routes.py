"""
inspect_extracted_routes.py

Inspect extracted GTFS route-stop sequences and enrich with stop names.

This script loads route-stop sequences extracted from stop_times.txt and trips.txt,
joins stop IDs with human-readable stop names from stops.txt, and saves a preview
for inspection and further analysis.

Usage:
    Run this script after `extract_routes_from_gtfs.py` to verify extracted routes.

Author: Onur Deniz (PhD Project)
"""

import pandas as pd
import logging
from pathlib import Path

# === Setup logging ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# === File paths ===
EXTRACTED_ROUTES_FILE = Path("data/processed/routes/extracted_gtfs_routes.csv")
STOPS_FILE = Path("data/raw/swiss/gtfs_ftp_2025/stops.txt")
OUTPUT_FILE = Path("data/processed/routes/enriched_gtfs_routes_with_names.csv")

def load_extracted_routes() -> pd.DataFrame:
    """
    Load extracted route-stop sequences.
    The stop_sequence column contains a list of stop_ids (as a string).
    """
    logging.info(f"📂 Loading extracted routes from {EXTRACTED_ROUTES_FILE}")
    return pd.read_csv(EXTRACTED_ROUTES_FILE, converters={"stop_sequence": eval})


def load_stop_names() -> pd.DataFrame:
    """
    Load stop ID to stop name mapping from GTFS stops.txt.
    """
    logging.info(f"📂 Loading stop names from {STOPS_FILE}")
    return pd.read_csv(STOPS_FILE, usecols=["stop_id", "stop_name"])


def enrich_with_stop_names(routes_df: pd.DataFrame, stops_df: pd.DataFrame) -> pd.DataFrame:
    """
    Explodes stop_sequence and merges each stop_id with its name.
    Returns a long-form dataframe with one row per stop in each trip.
    """
    logging.info("🔗 Joining stop names to extracted routes...")

    # Explode stop_sequence to individual rows
    exploded = routes_df.explode("stop_sequence").rename(columns={"stop_sequence": "stop_id"})

    # Merge with stop names
    enriched = exploded.merge(stops_df, on="stop_id", how="left")

    # Rename for clarity
    enriched = enriched.rename(columns={"stop_name": "stop_name_enriched"})

    return enriched


def save_enriched_routes(df: pd.DataFrame):
    """
    Save the enriched route-stop data to CSV for inspection.
    """
    logging.info(f"💾 Saving enriched routes to {OUTPUT_FILE}")
    df.to_csv(OUTPUT_FILE, index=False)
    logging.info("✅ Enriched route-stop data saved.")


def main():
    routes_df = load_extracted_routes()
    stops_df = load_stop_names()
    df_enriched = enrich_with_stop_names(routes_df, stops_df)
    save_enriched_routes(df_enriched)


if __name__ == "__main__":
    main()
