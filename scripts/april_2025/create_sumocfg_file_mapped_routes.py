"""
create_sumocfg_file_mapped_routes.py

Generates a SUMO config file using the newly matched route files (mapped_rou) for reliable simulation.
Each mapped .rou.xml is included.
Author: GPT-4 + Onur | April 2025
"""

import os
import xml.etree.ElementTree as ET
import logging
import glob

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# -------------------------------
# Paths
# -------------------------------
BASE_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024"
INPUT_PATH = os.path.join(BASE_PATH, "sumo", "inputs", "april_2025_swiss")
ROUTE_FOLDER = os.path.join(BASE_PATH, "data", "processed", "routes", "mapped_rou")
VEHICLE_FILE = os.path.join(BASE_PATH, "data", "processed", "routes", "vehicle_types.veh.xml")
NET_FILE = os.path.join(INPUT_PATH, "april_2025_swiss.net.xml")
OUTPUT_CFG = os.path.join(INPUT_PATH, "april_2025_swiss_mapped.sumocfg")
TRIPINFO_OUT = os.path.join(BASE_PATH, "sumo", "outputs", "april_2025_swiss", "tripinfo.xml")
STOPINFO_OUT = os.path.join(BASE_PATH, "sumo", "outputs", "april_2025_swiss", "stopinfo.xml")

# -------------------------------
# Script
# -------------------------------

def generate_config():
    logging.info("🔧 Generating SUMO config using mapped GTFS route files...")

    # Collect all route files
    route_files = sorted(glob.glob(os.path.join(ROUTE_FOLDER, "*.rou.xml")))
    if not route_files:
        logging.error("❌ No mapped route files found.")
        return

    logging.info(f"✅ Found {len(route_files)} mapped route files.")

    root = ET.Element("configuration")

    input_ = ET.SubElement(root, "input")
    ET.SubElement(input_, "net-file", value=NET_FILE)
    ET.SubElement(input_, "route-files", value=",".join(route_files))
    ET.SubElement(input_, "additional-files", value=VEHICLE_FILE)

    output = ET.SubElement(root, "output")
    ET.SubElement(output, "tripinfo-output", value=TRIPINFO_OUT)
    ET.SubElement(output, "stop-output", value=STOPINFO_OUT)

    time = ET.SubElement(root, "time")
    ET.SubElement(time, "begin", value="0")
    ET.SubElement(time, "end", value="36000")

    report = ET.SubElement(root, "report")
    ET.SubElement(report, "verbose", value="true")
    ET.SubElement(report, "no-step-log", value="true")

    # Save
    tree = ET.ElementTree(root)
    os.makedirs(os.path.dirname(OUTPUT_CFG), exist_ok=True)
    tree.write(OUTPUT_CFG, encoding="utf-8", xml_declaration=True)

    logging.info(f"✅ SUMO config saved to: {OUTPUT_CFG}")


if __name__ == "__main__":
    generate_config()
