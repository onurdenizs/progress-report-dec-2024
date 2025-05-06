"""
Script to build a vehicle profile table from filtered SBB vehicle data.
Extracts relevant parameters per vehicle type (rollmaterial code) and aggregates them.
"""

import pandas as pd
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Input/output paths
INPUT_FILE = Path("data/processed/routes/filtered_vehicle_data_for_simulation.csv")
OUTPUT_FILE = Path("data/processed/routes/vehicle_profile_table.csv")

def main():
    logging.info("📂 Loading filtered vehicle dataset...")
    df = pd.read_csv(INPUT_FILE, low_memory=False)

    logging.info("🔍 Selecting relevant vehicle parameters...")

    columns_to_use = [
        "rollmaterial",                         # Vehicle type key
        "Train_clean",                          # Cleaned train number (optional for traceability)
        "Tare (empty weight)",                  # Weight in tons
        "Length over train",                    # Length in mm
        "Operational Vmax in km/h",             # Max operating speed
        "Seats 1.cl. total train",
        "Seats 2.cl. total train",
        "Total wheelchair spaces NS/S",
        "Dining space in dining car per train",
        "Bike hooks",
        "Bike securing strap (standing zone)"
    ]

    df = df[columns_to_use]

    logging.info("📊 Grouping by 'rollmaterial' and aggregating averages...")
    grouped = df.groupby("rollmaterial").agg("mean").reset_index()

    grouped = grouped.rename(columns={
        "Tare (empty weight)": "avg_weight_tons",
        "Length over train": "avg_length_mm",
        "Operational Vmax in km/h": "avg_vmax_kmh",
        "Seats 1.cl. total train": "seats_1st_class",
        "Seats 2.cl. total train": "seats_2nd_class",
        "Total wheelchair spaces NS/S": "wheelchair_spaces",
        "Dining space in dining car per train": "dining_spaces",
        "Bike hooks": "bike_hooks",
        "Bike securing strap (standing zone)": "bike_straps"
    })

    grouped = grouped.round(2)

    logging.info("💾 Saving vehicle profile table to: %s", OUTPUT_FILE)
    grouped.to_csv(OUTPUT_FILE, index=False)
    logging.info("✅ Done.")

if __name__ == "__main__":
    main()
