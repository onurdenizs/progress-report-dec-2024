"""
define_kpi_metrics.py

Parses SUMO simulation output files to compute performance KPIs for trains:
- Total travel time per train
- Average speed
- Dwell time at each stop
- Headway between trains at key stations
- (Optional) emissions/energy placeholder

Saves results as CSVs in: outputs/kpi_results/

Author: GPT-4 + Onur | April 2025
"""

import os
import logging
import xml.etree.ElementTree as ET
import pandas as pd
from collections import defaultdict

# -------------------------
# Configuration
# -------------------------

TRIPINFO_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\outputs\sumo\tripinfo.xml"
STOPINFO_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\outputs\sumo\stopinfo.xml"
EMISSIONS_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\outputs\sumo\emissions.xml"  # Optional

OUTPUT_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\outputs\kpi_results"
os.makedirs(OUTPUT_DIR, exist_ok=True)

KEY_STOPS = ["edge_8503000", "edge_8501120", "edge_8501008", "edge_8507000"]  # Example: Genève, Lausanne, Zürich HB, Basel SBB

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


# -------------------------
# KPI 1 + 2: Travel Time & Speed
# -------------------------

def parse_tripinfo(file_path):
    logging.info("📈 Parsing tripinfo.xml...")
    tree = ET.parse(file_path)
    root = tree.getroot()

    rows = []
    for trip in root.findall("tripinfo"):
        vid = trip.attrib["id"]
        depart = float(trip.attrib["depart"])
        arrival = float(trip.attrib["arrival"])
        duration = arrival - depart
        speed = float(trip.attrib.get("speed", 0))
        distance = float(trip.attrib.get("routeLength", 0))
        rows.append([vid, depart, arrival, duration, distance, speed])

    df = pd.DataFrame(rows, columns=["train_id", "depart", "arrival", "total_travel_time", "route_length", "average_speed"])
    df.to_csv(os.path.join(OUTPUT_DIR, "travel_time.csv"), index=False)
    logging.info("💾 Saved: travel_time.csv")
    return df


# -------------------------
# KPI 3: Dwell Time per Stop
# -------------------------

def parse_stopinfo(file_path):
    logging.info("🚉 Parsing stopinfo.xml...")
    tree = ET.parse(file_path)
    root = tree.getroot()

    rows = []
    for stop in root.findall("stopinfo"):
        train = stop.attrib["id"]
        edge = stop.attrib["edge"]
        arrival = float(stop.attrib["arrival"])
        departure = float(stop.attrib["departure"])
        duration = departure - arrival
        rows.append([train, edge, arrival, departure, duration])

    df = pd.DataFrame(rows, columns=["train_id", "stop_edge", "arrival_time", "departure_time", "dwell_time"])
    df.to_csv(os.path.join(OUTPUT_DIR, "dwell_time.csv"), index=False)
    logging.info("💾 Saved: dwell_time.csv")
    return df


# -------------------------
# KPI 4: Headway at Key Stops
# -------------------------

def compute_headways(stop_df):
    logging.info("🔗 Computing headways at key stations...")
    headways = []

    for stop in KEY_STOPS:
        df_key = stop_df[stop_df["stop_edge"] == stop].sort_values("arrival_time")
        arrivals = df_key["arrival_time"].tolist()

        for i in range(1, len(arrivals)):
            gap = arrivals[i] - arrivals[i - 1]
            headways.append([stop, arrivals[i], gap])

    df_hw = pd.DataFrame(headways, columns=["station_edge", "arrival_time", "headway_sec"])
    df_hw.to_csv(os.path.join(OUTPUT_DIR, "headways.csv"), index=False)
    logging.info("💾 Saved: headways.csv")
    return df_hw


# -------------------------
# (Optional) KPI 5: Emissions (Placeholder)
# -------------------------

def parse_emissions(file_path):
    if not os.path.exists(file_path):
        logging.warning("⚠️ emissions.xml not found. Skipping emissions KPI.")
        return None

    logging.info("🌫️ Parsing emissions.xml... (not yet implemented in detail)")
    # Implementation depends on SUMO vehicle emission settings
    return None


# -------------------------
# Main
# -------------------------

def main():
    trip_df = parse_tripinfo(TRIPINFO_PATH)
    stop_df = parse_stopinfo(STOPINFO_PATH)
    compute_headways(stop_df)
    parse_emissions(EMISSIONS_PATH)  # Optional

    logging.info("✅ KPI extraction complete.")

if __name__ == "__main__":
    main()
