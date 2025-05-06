"""
generate_randomized_sumo_routes.py

Generates SUMO-compatible .rou.xml and .veh.xml files for selected Swiss IC/IR routes.
Randomizes departure times and dwell times. Assigns vehicle types from a predefined pool.

Input:
- stop_sequences/*.csv per selected route (with stop_id and stop_sequence)
- SUMO edge IDs should match stop_id format
- Optional: hardcoded or later-loaded vehicle profiles

Output:
- selected_intercity_routes.rou.xml
- vehicle_types.veh.xml

Author: GPT-4 + Onur | April 2025
"""

import os
import random
import logging
import xml.etree.ElementTree as ET
import pandas as pd

# -------------------------
# Configuration
# -------------------------

STOP_SEQ_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\stop_sequences"
ROUTE_OUTPUT = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\selected_intercity_routes.rou.xml"
VEHICLE_OUTPUT = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\vehicle_types.veh.xml"

# Basic vehicle pool (can be expanded with real SBB formation data later)
VEHICLE_TYPES = {
    "ic_double_deck": {"length": "200.0", "accel": "0.8", "decel": "1.0", "maxSpeed": "55.56"},  # 200 km/h
    "ir_single_deck": {"length": "150.0", "accel": "0.9", "decel": "1.2", "maxSpeed": "44.44"},  # 160 km/h
}

# Departure window and stop dwell range
DEPARTURE_START = 6 * 3600  # 06:00 in seconds
DEPARTURE_END = 10 * 3600   # 10:00 in seconds
DWELL_MIN = 30  # seconds
DWELL_MAX = 90  # seconds

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def generate_vehicle_type_xml():
    logging.info("🚧 Generating vehicle types...")
    root = ET.Element("vTypeDistribution", id="train_types")

    for veh_id, attrs in VEHICLE_TYPES.items():
        vtype = ET.SubElement(root, "vType", id=veh_id, **attrs)
        vtype.set("vClass", "rail")

    tree = ET.ElementTree(root)
    tree.write(VEHICLE_OUTPUT, encoding="utf-8", xml_declaration=True)
    logging.info(f"💾 Saved vehicle types to: {VEHICLE_OUTPUT}")


def generate_route_file():
    logging.info("🚧 Generating .rou.xml route file...")
    root = ET.Element("routes")

    # Reference vehicle types
    for veh_id, attrs in VEHICLE_TYPES.items():
        ET.SubElement(root, "vType", id=veh_id, **attrs, vClass="rail")

    trip_id = 0
    for file in os.listdir(STOP_SEQ_DIR):
        if not file.endswith(".csv"):
            continue

        route_id = file.replace("_stops.csv", "")
        df = pd.read_csv(os.path.join(STOP_SEQ_DIR, file))
        if df.empty or len(df) < 2:
            logging.warning(f"⚠️ Skipping route {route_id}: too few stops.")
            continue

        edge_list = [f"edge_{stop_id}" for stop_id in df["stop_id"].tolist()]
        route_str = " ".join(edge_list)

        # Assign vehicle type
        veh_type = "ic_double_deck" if "IC" in route_id else "ir_single_deck"

        # Departure time
        depart = random.randint(DEPARTURE_START, DEPARTURE_END)

        # Define vehicle
        veh_elem = ET.SubElement(root, "vehicle", id=f"train_{trip_id}", type=veh_type, depart=str(depart))
        ET.SubElement(veh_elem, "route", edges=route_str)

        # Add stops with dwell times
        for stop_id in df["stop_id"]:
            ET.SubElement(veh_elem, "stop", lane=f"edge_{stop_id}_0",
                          duration=str(random.randint(DWELL_MIN, DWELL_MAX)))

        trip_id += 1

    tree = ET.ElementTree(root)
    tree.write(ROUTE_OUTPUT, encoding="utf-8", xml_declaration=True)
    logging.info(f"💾 Saved route file to: {ROUTE_OUTPUT}")


def main():
    generate_vehicle_type_xml()
    generate_route_file()
    logging.info("✅ Phase 3 complete: Route + vehicle generation ready.")


if __name__ == "__main__":
    main()
