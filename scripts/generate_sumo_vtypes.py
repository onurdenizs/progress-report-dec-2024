"""
Generate SUMO-compatible vehicle type definitions from the vehicle profile table.

This script reads the cleaned vehicle profile table (from SBB datasets)
and generates a .veh.xml file with <vType> definitions for SUMO.
"""

import pandas as pd
from lxml import etree
import logging
from pathlib import Path

# Setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Input/output paths
INPUT_FILE = Path("data/processed/routes/vehicle_profile_table.csv")
OUTPUT_FILE = Path("data/processed/routes/vehicle_types.veh.xml")

def generate_vehicle_type_element(row: pd.Series) -> etree.Element:
    """
    Generate a <vType> XML element for SUMO using parameters from a vehicle row.
    Falls back to defaults if values are missing.
    """
    vehicle_id = str(row["rollmaterial"]).strip().replace(" ", "_")

    # Extract values with fallbacks
    max_speed = row.get("Operational Vmax in km/h", 160)
    length = row.get("Length over train", 10000) / 1000  # convert mm to meters
    capacity = row.get("Sitzplätze pro Zug Total", 300)

    return etree.Element(
        "vType",
        id=vehicle_id,
        vClass="rail",
        accel="0.8",
        decel="1.0",
        sigma="0.5",
        length=str(round(length, 2)),
        maxSpeed=str(round(max_speed, 1)),
        personCapacity=str(int(capacity))
    )

def main():
    logging.info("📂 Loading vehicle profile table...")
    df = pd.read_csv(INPUT_FILE)

    logging.info(f"✅ Loaded {len(df)} vehicle profiles. Generating XML...")

    # XML structure
    root = etree.Element("vehicleTypes")
    for _, row in df.iterrows():
        vtype_elem = generate_vehicle_type_element(row)
        root.append(vtype_elem)

    tree = etree.ElementTree(root)
    tree.write(OUTPUT_FILE, pretty_print=True, xml_declaration=True, encoding="UTF-8")
    logging.info(f"✅ Written vehicle types to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
