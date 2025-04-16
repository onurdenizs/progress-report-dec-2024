import pandas as pd
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# === File paths ===
SUMMARY_FILE = "data/processed/routes/route_summary_stats.csv"

def main():
    logging.info(f"📂 Loading route summary from {SUMMARY_FILE}")
    df = pd.read_csv(SUMMARY_FILE)

    logging.info("🔢 Top 10 routes by total trip volume:")
    top_volume = df.sort_values("total_trips", ascending=False).head(10)
    print(top_volume[["route_id", "total_trips", "avg_stops_per_trip"]])

    logging.info("\n🛤️ Top 10 routes by average stops per trip:")
    top_length = df.sort_values("avg_stops_per_trip", ascending=False).head(10)
    print(top_length[["route_id", "total_trips", "avg_stops_per_trip"]])

    logging.info("\n🧠 Recommended candidates (intersection of both groups):")
    top_candidates = pd.merge(top_volume, top_length, on="route_id", how="inner")
    print(top_candidates[["route_id", "total_trips_x", "avg_stops_per_trip_x"]])

if __name__ == "__main__":
    main()
