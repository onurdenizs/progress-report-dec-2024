"""
Assign realistic vehicle types to <trip> elements in a SUMO .rou.xml route file,
based on a route-to-vehicle_type mapping.

This script runs in the user's local environment, with GTFS route IDs and vehicle type
info coming from the mapping CSV.
"""

import pandas as pd
import xml.etree.ElementTree as ET
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# File paths
ROUTE_FILE_IN = "data/processed/routes/selected_intercity_routes.rou.xml"
ROUTE_FILE_OUT = "data/processed/routes/selected_intercity_routes_with_types.rou.xml"
MAPPING_CSV = "data/processed/routes/vehicle_type_mapping.csv"

def main():
    logging.info("📂 Loading route-to-vehicle mapping...")
    df_map = pd.read_csv(MAPPING_CSV)
    route_to_type = dict(zip(df_map["route_id"], df_map["vehicle_type"]))

    logging.info("📂 Parsing SUMO .rou.xml file...")
    tree = ET.parse(ROUTE_FILE_IN)
    root = tree.getroot()

    updated_count = 0

    # Update <trip> elements with correct vehicle types based on route_id
    for trip in root.findall("trip"):
        route_id = trip.get("id")
        if not route_id:
            continue
        # Get route_id from trip id (e.g., "1.TA.91-5-A-j25-1.1.H" → "91-5-A-j25-1")
        parts = route_id.split(".")
        if len(parts) >= 3:
            route_key = parts[2]
            if route_key in route_to_type:
                trip.set("type", route_to_type[route_key])
                updated_count += 1

    logging.info(f"✅ Updated vehicle types for {updated_count} <trip> elements.")

    logging.info(f"💾 Writing updated route file to: {ROUTE_FILE_OUT}")
    tree.write(ROUTE_FILE_OUT, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    main()
