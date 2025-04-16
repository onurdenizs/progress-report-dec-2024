"""
match_vehicle_types_heuristic.py

Infers likely train vehicle types (e.g., IC, IR, RE) for each inter-city route
based on average number of stops per trip using simple heuristics.

Designed to work with selected_intercity_routes.csv.
"""

import pandas as pd
from pathlib import Path
import logging

# === Setup logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# === File paths ===
INPUT_CSV = Path("data/processed/routes/selected_intercity_routes.csv")
OUTPUT_CSV = Path("data/processed/routes/vehicle_type_mapping.csv")

def infer_vehicle_class(avg_stops: float) -> str:
    """
    Apply simple heuristic to infer train vehicle class.
    """
    if avg_stops <= 5:
        return "IC"  # InterCity
    elif avg_stops <= 10:
        return "IR"  # InterRegio
    else:
        return "RE"  # RegioExpress

def main():
    logging.info("📂 Reading selected inter-city GTFS data...")
    df = pd.read_csv(INPUT_CSV)

    logging.info("🔍 Aggregating number of stops per trip...")
    trip_stops = df.groupby(["route_id", "trip_id"]).size().reset_index(name="num_stops")

    logging.info("📊 Aggregating stop statistics per route...")
    route_summary = (
        trip_stops.groupby("route_id")["num_stops"]
        .agg(["mean", "min", "max", "count"])
        .reset_index()
        .rename(columns={"mean": "avg_stops", "count": "trip_count"})
    )

    logging.info("🚆 Applying vehicle class heuristics...")
    route_summary["vehicle_type"] = route_summary["avg_stops"].apply(infer_vehicle_class)

    logging.info("💾 Saving vehicle type mapping to %s", OUTPUT_CSV)
    route_summary.to_csv(OUTPUT_CSV, index=False)

    logging.info("✅ Vehicle type mapping complete.")

if __name__ == "__main__":
    main()
