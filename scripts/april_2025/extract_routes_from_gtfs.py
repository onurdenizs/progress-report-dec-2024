"""
extract_routes_from_gtfs.py

Extracts Swiss intercity train routes from GTFS data and summarizes:
- Route IDs and names
- Origin and destination
- Intermediate stops
- Trip frequency

Output:
- cleaned_routes_summary.csv (all routes)
- top_intercity_candidates.csv (filtered high-volume routes)
- individual route stop sequences saved as separate files

Author: GPT-4 + Onur, April 2025
"""

import pandas as pd
import logging
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Paths
GTFS_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\gtfs_ftp_2025"
OUTPUT_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def main():
    logging.info("📥 Loading GTFS files...")
    routes = pd.read_csv(os.path.join(GTFS_DIR, "routes.txt"))
    trips = pd.read_csv(os.path.join(GTFS_DIR, "trips.txt"))
    stop_times = pd.read_csv(os.path.join(GTFS_DIR, "stop_times.txt"))
    stops = pd.read_csv(os.path.join(GTFS_DIR, "stops.txt"))

    logging.info("🔗 Merging trips with route info...")
    trip_route = trips.merge(routes, on="route_id", how="left")

    logging.info("📌 Grouping stop sequences...")
    stop_times_sorted = stop_times.sort_values(["trip_id", "stop_sequence"])
    trip_stops = stop_times_sorted.groupby("trip_id")["stop_id"].apply(list).reset_index()

    logging.info("🔍 Counting trips per route...")
    route_trip_counts = trip_route["route_id"].value_counts().rename("trip_count").reset_index()
    route_trip_counts.columns = ["route_id", "trip_count"]
    routes_summary = trip_route.drop_duplicates("route_id").merge(route_trip_counts, on="route_id")

    logging.info("💾 Saving cleaned route summary...")
    routes_summary.to_csv(os.path.join(OUTPUT_DIR, "cleaned_routes_summary.csv"), index=False)

    # ✅ Filter likely intercity rail routes based on naming heuristics
    logging.info("🧠 Filtering intercity route candidates (IC, IR, RE)...")
    intercity_mask = routes_summary["route_short_name"].str.contains(r"\b(IC|IR|RE)\b", case=False, na=False)
    intercity_routes = routes_summary[intercity_mask]
    intercity_routes.to_csv(os.path.join(OUTPUT_DIR, "top_intercity_candidates.csv"), index=False)

    logging.info(f"✅ Found {len(intercity_routes)} intercity candidates.")
    logging.info("🔄 Saving individual route stop sequences for inspection...")

    for _, route_row in intercity_routes.iterrows():
        route_id = route_row["route_id"]
        trip_ids = trips[trips["route_id"] == route_id]["trip_id"].unique()
        if len(trip_ids) == 0:
            continue
        one_trip_id = trip_ids[0]
        stop_seq = stop_times_sorted[stop_times_sorted["trip_id"] == one_trip_id].merge(
            stops, on="stop_id", how="left"
        )
        stop_seq.to_csv(os.path.join(OUTPUT_DIR, f"route_{route_id}_stops.csv"), index=False)

    logging.info("🎯 Phase 1 complete: Real-world routes extracted.")

if __name__ == "__main__":
    main()
