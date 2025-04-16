"""
inspect_vehicle_type_mapping.py

This script loads and summarizes the vehicle type mappings produced using GTFS heuristics,
allowing you to inspect route volumes and stop statistics for selected inter-city trains.

Author: Onur Deniz & ChatGPT Co-Pilot
"""

import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# File path
FILE = Path("data/processed/routes/vehicle_type_mapping.csv")

def main():
    """Load and display vehicle type mapping statistics."""
    logging.info(f"📂 Reading vehicle type mapping from {FILE}")
    df = pd.read_csv(FILE)

    # Preview first few rows
    logging.info("📊 Preview of mapping table:")
    print(df.head(10).to_string(index=False))

    # Frequency count of each vehicle type
    logging.info("🧾 Available vehicle types and route counts:")
    print(df["vehicle_type"].value_counts().to_string())

    # Summarize per route
    logging.info("🔁 Summary table sorted by trip count:")
    summary = df[["route_id", "trip_count", "avg_stops", "vehicle_type"]]
    summary = summary.sort_values("trip_count", ascending=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
