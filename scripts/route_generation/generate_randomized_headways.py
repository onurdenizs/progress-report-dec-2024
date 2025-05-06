"""
Generate randomized headway-based departures and stop durations for SUMO inter-city routes.

Reads selected_intercity_routes.csv, assigns randomized headways, stop durations, and 
optional jitter to departure times and positions. Outputs SUMO-compatible .rou.xml file.

Author: ChatGPT / Onur
"""

import pandas as pd
import xml.etree.ElementTree as ET
import os
import random
import logging

# ─────────────────────────────────────────────────────────────
# CONFIGURATION: MIN/MAX for randomness
# ─────────────────────────────────────────────────────────────
HEADWAY_MIN = 180  # seconds (3 minutes)
HEADWAY_MAX = 600  # seconds (10 minutes)
STOP_DURATION_MIN = 10  # seconds
STOP_DURATION_MAX = 60  # seconds
DEPARTURE_JITTER = 5     # ± seconds jitter
STOP_OFFSET_JITTER = 2   # ± meters offset (not critical in SUMO rail)

# ─────────────────────────────────────────────────────────────
# PATHS (adjust only if needed)
# ─────────────────────────────────────────────────────────────
INPUT_CSV = "data/processed/routes/selected_intercity_routes.csv"
OUTPUT_XML = "data/processed/routes/randomized_intercity_routes.rou.xml"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ─────────────────────────────────────────────────────────────
# Main logic
# ─────────────────────────────────────────────────────────────
def generate_randomized_routes():
    logging.info("📂 Loading selected inter-city route data...")
    df = pd.read_csv(INPUT_CSV)

    logging.info(f"✅ Loaded {df.shape[0]} stop records.")

    root = ET.Element("routes")
    grouped = df.groupby("trip_id")
    time_counter = {}

    for trip_id, group in grouped:
        group_sorted = group.sort_values("stop_sequence")
        route_id = group_sorted.iloc[0]["route_id"]
        origin_stop = group_sorted.iloc[0]["stop_id"]

        # Generate a unique vehicle ID
        vehicle_id = f"{trip_id}"

        # Determine randomized headway
        if route_id not in time_counter:
            time_counter[route_id] = 0
        depart_time = time_counter[route_id] + random.randint(-DEPARTURE_JITTER, DEPARTURE_JITTER)
        headway = random.randint(HEADWAY_MIN, HEADWAY_MAX)
        time_counter[route_id] += headway

        trip_elem = ET.SubElement(root, "trip", {
            "id": vehicle_id,
            "type": "default",  # or use actual vehicle type mappings
            "depart": str(max(0, depart_time)),  # no negative times
            "from": group_sorted.iloc[0]["stop_id"],
            "to": group_sorted.iloc[-1]["stop_id"],
        })

        # Add stop elements
        for _, row in group_sorted.iterrows():
            duration = random.randint(STOP_DURATION_MIN, STOP_DURATION_MAX)
            offset = round(random.uniform(-STOP_OFFSET_JITTER, STOP_OFFSET_JITTER), 2)
            ET.SubElement(trip_elem, "stop", {
                "busStop": row["stop_id"],
                "duration": str(duration),
                "until": "",  # optional
                "parking": "true",
                "until": "",
                "lat": "", "lon": "",
                "startPos": str(offset)  # optional
            })

    logging.info(f"💾 Writing randomized route XML to: {OUTPUT_XML}")
    tree = ET.ElementTree(root)
    os.makedirs(os.path.dirname(OUTPUT_XML), exist_ok=True)
    tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)
    logging.info("✅ Done.")

# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    generate_randomized_routes()
