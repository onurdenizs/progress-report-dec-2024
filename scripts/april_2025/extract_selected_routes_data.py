"""
extract_selected_routes_data.py

Extracts stop sequences with station names for selected GTFS route_ids.
Outputs a CSV for each selected route showing the trip_id, stop_id, stop_name,
stop_sequence, arrival_time, and departure_time.

Author: GPT-4 + Onur | April 2025
"""

import os
import pandas as pd
import logging

# -------------------------
# Configuration
# -------------------------

GTFS_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\gtfs_ftp_2025"
OUTPUT_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\stop_sequences"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Your selected route_ids (3 IC, 2 IR)
SELECTED_ROUTE_IDS = [
    "91-19-Y-j25-1",
    "91-2H-Y-j25-1",
    "91-29-Y-j25-1",
    "91-2Q-Y-j25-1",
    "91-3M-Y-j25-1"
]

# -------------------------
# Setup Logging
# -------------------------

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# -------------------------
# Main Script
# -------------------------

def main():
    logging.info("📥 Loading GTFS files...")
    trips = pd.read_csv(os.path.join(GTFS_DIR, "trips.txt"))
    stop_times = pd.read_csv(os.path.join(GTFS_DIR, "stop_times.txt"))
    stops = pd.read_csv(os.path.join(GTFS_DIR, "stops.txt"))

    logging.info("🔍 Matching route_ids to trip_ids...")
    for route_id in SELECTED_ROUTE_IDS:
        route_trips = trips[trips["route_id"] == route_id]
        if route_trips.empty:
            logging.warning(f"⚠️ No trips found for route_id: {route_id}")
            continue

        # Pick first valid trip_id
        trip_id = route_trips.iloc[0]["trip_id"]
        logging.info(f"🛤️ Route: {route_id} → Using trip_id: {trip_id}")

        trip_stops = stop_times[stop_times["trip_id"] == trip_id]
        if trip_stops.empty:
            logging.warning(f"⚠️ No stop_times found for trip_id: {trip_id}")
            continue

        # Join with stop names
        merged = trip_stops.merge(stops, on="stop_id", how="left")
        merged = merged.sort_values("stop_sequence")

        # Select useful columns
        output_df = merged[[
            "trip_id", "stop_sequence", "stop_id", "stop_name", "arrival_time", "departure_time"
        ]]

        output_path = os.path.join(OUTPUT_DIR, f"{route_id}_stops.csv")
        output_df.to_csv(output_path, index=False)
        logging.info(f"💾 Saved: {output_path} ({len(output_df)} stops)")

    logging.info("✅ All selected routes processed.")

if __name__ == "__main__":
    main()
