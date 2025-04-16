"""
Investigate selected GTFS routes in detail:
- Total trips per route
- Representative trip_id
- Origin, destination, and stop sequence (with names)
"""

import pandas as pd
import logging

# Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

ENRICHED_STOP_TIMES = "data/processed/routes/cleaned_stop_times_enriched.csv"
STOPS_FILE = "data/raw/swiss/gtfs_ftp_2025/stops.txt"

SELECTED_ROUTES = [
    "92-449-A-j25-1",
    "92-N1-E-j25-1",
    "92-670-j25-1"
]

def main():
    logging.info(f"📂 Loading enriched stop_times from {ENRICHED_STOP_TIMES}")
    df = pd.read_csv(ENRICHED_STOP_TIMES)

    logging.info(f"📂 Loading stop names from {STOPS_FILE}")
    df_stops = pd.read_csv(STOPS_FILE, usecols=["stop_id", "stop_name"])

    logging.info(f"🔗 Joining stop names...")
    df = df.merge(df_stops, on="stop_id", how="left")

    df_selected = df[df["route_id"].isin(SELECTED_ROUTES)]
    logging.info(f"✅ Found {len(df_selected)} rows for selected routes")

    for route in SELECTED_ROUTES:
        df_route = df_selected[df_selected["route_id"] == route]
        trip_counts = df_route["trip_id"].nunique()
        representative_trip = df_route["trip_id"].value_counts().idxmax()
        df_trip = df_route[df_route["trip_id"] == representative_trip].sort_values("stop_sequence")

        origin = df_trip.iloc[0]["stop_name"]
        destination = df_trip.iloc[-1]["stop_name"]
        stops = df_trip["stop_name"].tolist()

        logging.info(f"\n🛤️ Route: {route}")
        logging.info(f"🔁 Total trips: {trip_counts}")
        logging.info(f"📌 Representative trip_id: {representative_trip}")
        logging.info(f"➡️ Origin: {origin}")
        logging.info(f"⛳ Destination: {destination}")
        logging.info(f"📍 Stops ({len(stops)}): {', '.join(stops)}")

if __name__ == "__main__":
    main()
