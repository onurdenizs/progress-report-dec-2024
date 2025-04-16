"""
extract_routes_from_gtfs.py

This script processes the enriched GTFS stop_times data to extract
origin-destination (OD) pairs along with full stop sequences for each trip.
It outputs a structured CSV listing route_id, trip_id, origin_stop_id,
destination_stop_id, and the ordered list of intermediate stops.

Author: Onur Deniz
"""

import pandas as pd
import logging
from pathlib import Path
from ast import literal_eval

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# === File Paths ===
INPUT_FILE = Path("data/processed/routes/cleaned_stop_times_enriched.csv")
OUTPUT_FILE = Path("data/processed/routes/extracted_gtfs_routes.csv")

def extract_routes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts origin, destination, and ordered stops from the GTFS dataframe.

    Args:
        df (pd.DataFrame): Merged GTFS stop_times + trips data.

    Returns:
        pd.DataFrame: DataFrame with route_id, trip_id, origin_stop_id,
                      destination_stop_id, and stop_sequence list.
    """
    logging.info("🔄 Grouping by route_id and trip_id...")
    grouped = df.sort_values(["trip_id", "stop_sequence"]).groupby(["route_id", "trip_id"])

    extracted = []
    for (route_id, trip_id), group in grouped:
        stop_ids = group["stop_id"].tolist()
        if len(stop_ids) >= 2:  # Ignore malformed/short trips
            extracted.append({
                "route_id": route_id,
                "trip_id": trip_id,
                "origin_stop_id": stop_ids[0],
                "destination_stop_id": stop_ids[-1],
                "stop_sequence": stop_ids
            })

    return pd.DataFrame(extracted)

def main():
    logging.info(f"🚀 Loading enriched stop_times from {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE)

    logging.info("✅ Data loaded. Extracting routes...")
    routes_df = extract_routes(df)

    logging.info(f"💾 Saving extracted routes to {OUTPUT_FILE}")
    routes_df.to_csv(OUTPUT_FILE, index=False)
    logging.info("✅ Route extraction complete.")

if __name__ == "__main__":
    main()
