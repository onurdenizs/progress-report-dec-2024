"""
create_sumocfg_file_mapped_routes_kpis.py

Generates a SUMO config (.sumocfg) referencing the corrected GTFS-mapped routes
and enables KPI outputs like tripinfo.xml. Includes internal logging for stop events.

Author: GPT-4 + Onur | Updated May 2025
"""

import os
import logging
import glob
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ------------------ Config ------------------

CONFIG_NAME = "april_2025_swiss_mapped_kpis.sumocfg"

OUTPUT_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\april_2025_swiss"
ROUTE_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\mapped_rou"
VEHICLE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\vehicle_types.veh.xml"
NET_FILE = os.path.join(OUTPUT_PATH, "april_2025_swiss.net.xml")

OUTPUT_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\outputs\april_2025_swiss"
TRIPINFO_PATH = os.path.join(OUTPUT_DIR, "tripinfo.xml")

# ------------------ Main ------------------

def main():
    logging.info("🔧 Generating updated SUMO config with mapped routes and KPI outputs...")

    route_files = glob.glob(os.path.join(ROUTE_DIR, "*.rou.xml"))
    if not route_files:
        logging.error("❌ No mapped route files found!")
        return
    logging.info(f"✅ Found {len(route_files)} mapped route files.")

    root = ET.Element("configuration")

    # --- Input files ---
    input_elem = ET.SubElement(root, "input")
    ET.SubElement(input_elem, "net-file", value=NET_FILE)
    ET.SubElement(input_elem, "route-files", value=",".join(route_files))
    ET.SubElement(input_elem, "additional-files", value=VEHICLE_FILE)

    # --- Time settings ---
    time_elem = ET.SubElement(root, "time")
    ET.SubElement(time_elem, "begin", value="0")
    ET.SubElement(time_elem, "end", value="10000")  # adjust as needed

    # --- Output files ---
    output_elem = ET.SubElement(root, "output")
    ET.SubElement(output_elem, "tripinfo-output", value=TRIPINFO_PATH)

    # --- Enable stop event logging ---
    processing_elem = ET.SubElement(root, "processing")
    ET.SubElement(processing_elem, "device.stopManager.params", value="logStopStart,logStopEnd")

    # --- (Optional) Reporting ---
    ET.SubElement(root, "report", attrib={"log": "true"})

    # --- Save to disk ---
    config_tree = ET.ElementTree(root)
    config_file = os.path.join(OUTPUT_PATH, CONFIG_NAME)
    config_tree.write(config_file, encoding="utf-8", xml_declaration=True)

    logging.info(f"✅ SUMO config saved to: {config_file}")


if __name__ == "__main__":
    main()
