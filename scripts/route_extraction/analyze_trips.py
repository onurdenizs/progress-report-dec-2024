# scripts/route_extraction/analyze_trips.py

import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# === File paths ===
STOP_TIMES_FILE = Path("data/raw/swiss/gtfs_ftp_2025/stop_times.txt")
TRIPS_FILE = Path("data/raw/swiss/gtfs_ftp_2025/trips.txt")
OUTPUT_FILE = Path("data/processed/routes/cleaned_stop_times_enriched.csv")

def main():
    logging.info("🚀 Reading GTFS stop_times.txt...")
    stop_times = pd.read_csv(STOP_TIMES_FILE)
    logging.info(f"✅ Loaded {len(stop_times):,} rows from stop_times")

    logging.info("🚀 Reading GTFS trips.txt...")
    trips = pd.read_csv(TRIPS_FILE, low_memory=False)
    logging.info(f"✅ Loaded {len(trips):,} rows from trips")

    # Join with trips to enrich with route_id and headsign
    logging.info("🔗 Merging stop_times with trips on trip_id...")
    merged = stop_times.merge(
        trips[["trip_id", "route_id", "trip_headsign"]],
        how="left",
        on="trip_id"
    )

    logging.info(f"✅ Merged: {len(merged):,} rows")

    # Quick sample
    logging.info("🔍 Sample rows:")
    logging.info(merged.head(10).to_string())

    # Save to processed
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(OUTPUT_FILE, index=False)
    logging.info(f"💾 Saved cleaned + enriched stop_times to {OUTPUT_FILE.resolve()}")

if __name__ == "__main__":
    main()

