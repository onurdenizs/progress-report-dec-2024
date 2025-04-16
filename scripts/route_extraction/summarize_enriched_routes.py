"""
summarize_enriched_routes.py

Summarizes GTFS routes based on enriched GTFS stop-time data that includes stop IDs.

Computes per route_id:
- Total number of distinct trips
- Average number of stops per trip
- Most frequent destination stop IDs
"""

import pandas as pd
import logging
from pathlib import Path

# === Config ===
INPUT_FILE = Path("data/processed/routes/enriched_gtfs_routes_with_names.csv")
OUTPUT_FILE = Path("data/processed/routes/route_summary_stats.csv")

# === Logging ===
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    logging.info(f"📂 Loading enriched route-stop data from {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, low_memory=False)

    logging.info("🔄 Computing stop counts per trip...")
    trip_stop_counts = df.groupby(["route_id", "trip_id"]).size().reset_index(name="num_stops")

    logging.info("🔎 Aggregating per route_id...")
    summary = trip_stop_counts.groupby("route_id").agg(
        total_trips=("trip_id", "nunique"),
        avg_stops_per_trip=("num_stops", "mean"),
    ).reset_index()

    logging.info("📌 Identifying most common destination stop IDs...")
    dest_counts = df.groupby(["route_id", "destination_stop_id"]).size().reset_index(name="count")
    most_common_dest = dest_counts.sort_values(["route_id", "count"], ascending=[True, False])
    top_dests = most_common_dest.groupby("route_id").head(1)[["route_id", "destination_stop_id"]]
    top_dests.rename(columns={"destination_stop_id": "most_common_dest_stop_id"}, inplace=True)

    logging.info("🔗 Merging destination info into summary...")
    summary = summary.merge(top_dests, on="route_id", how="left")

    logging.info(f"💾 Saving summary to {OUTPUT_FILE}")
    summary.to_csv(OUTPUT_FILE, index=False)

    logging.info("✅ Done. Route summary generated.")

if __name__ == "__main__":
    main()
