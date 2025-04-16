"""
Script to inspect inter-city route candidates by showing their stop sequences,
origin-destination station names, and trip frequencies. Helps in manual selection
of simulation-worthy routes.

Author: Onur Deniz
Date: 2025-04-15
"""

import pandas as pd
import logging
from pathlib import Path

# ─── Setup ─────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ─── File Paths ─────────────────────────────────────────────────────────
INTERCITY_FILE = Path("data/processed/routes/intercity_route_candidates.csv")
STOP_TIMES_FILE = Path("data/processed/routes/cleaned_stop_times_enriched.csv")
STOPS_FILE = Path("data/raw/swiss/gtfs_ftp_2025/stops.txt")

# ─── Load Data ──────────────────────────────────────────────────────────
logging.info("📂 Loading inter-city route candidates...")
df_routes = pd.read_csv(INTERCITY_FILE)

logging.info("📂 Loading enriched stop_times...")
df_times = pd.read_csv(STOP_TIMES_FILE)

logging.info("📂 Loading stop name mapping...")
df_stops = pd.read_csv(STOPS_FILE)[["stop_id", "stop_name"]]

# ─── Join stop names ────────────────────────────────────────────────────
logging.info("🔗 Joining stop names...")
df_times = df_times.merge(df_stops, on="stop_id", how="left")

# ─── Filter for inter-city routes ───────────────────────────────────────
logging.info("🔍 Filtering stop_times to inter-city routes...")
intercity_ids = df_routes["route_id"].unique()
df_filtered = df_times[df_times["route_id"].isin(intercity_ids)]

# ─── Analyze and Print Summary ──────────────────────────────────────────
for route_id in intercity_ids:
    df_route = df_filtered[df_filtered["route_id"] == route_id]
    if df_route.empty:
        continue

    trip_counts = df_route["trip_id"].nunique()
    rep_trip_id = df_route["trip_id"].value_counts().idxmax()
    df_trip = df_route[df_route["trip_id"] == rep_trip_id].sort_values("stop_sequence")

    origin = df_trip.iloc[0]["stop_name"]
    destination = df_trip.iloc[-1]["stop_name"]
    stops = df_trip["stop_name"].tolist()

    logging.info(f"\n🛤️ Route: {route_id}")
    logging.info(f"🔁 Total trips: {trip_counts}")
    logging.info(f"📌 Representative trip_id: {rep_trip_id}")
    logging.info(f"➡️ Origin: {origin}")
    logging.info(f"⛳ Destination: {destination}")
    logging.info(f"📍 Number of stops: {len(stops)}")
    logging.info(f"📍 Stops: {', '.join(stops[:8])}... → ...{', '.join(stops[-3:])}")

# ─── End ────────────────────────────────────────────────────────────────
logging.info("✅ Done. You can now choose 3–5 routes to simulate.")
