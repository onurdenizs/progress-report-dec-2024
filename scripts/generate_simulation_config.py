"""
Generate a SUMO simulation configuration file (.sumocfg) for selected inter-city Swiss railway routes.
This script references the full absolute paths to the network, vehicle type, and route files.

Author: Onur Deniz
"""

import os
import logging
import xml.etree.ElementTree as ET

# -------------------- Configuration -------------------- #
NETWORK_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\rail_network.net.xml"
ROUTE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\selected_intercity_routes_with_types.rou.xml"
VTYPE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\vehicle_types.veh.xml"
OUTPUT_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\selected_intercity_simulation.sumocfg"

# -------------------- Setup Logger -------------------- #
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def generate_sumo_config():
    """
    Generate a SUMO configuration file linking the network, route, and vehicle type files
    using fully qualified absolute file paths.
    """
    logging.info("📁 Preparing to generate SUMO simulation config file...")
    
    root = ET.Element("configuration")

    # Input section
    input_elem = ET.SubElement(root, "input")
    ET.SubElement(input_elem, "net-file", value=NETWORK_FILE)
    ET.SubElement(input_elem, "route-files", value=f"{VTYPE_FILE},{ROUTE_FILE}")

    # Optional time section
    time_elem = ET.SubElement(root, "time")
    ET.SubElement(time_elem, "begin", value="0")
    ET.SubElement(time_elem, "end", value="3600")  # 1 hour of simulation

    # Write XML to file
    tree = ET.ElementTree(root)
    logging.info(f"💾 Writing SUMO config to: {OUTPUT_FILE}")
    tree.write(OUTPUT_FILE, encoding="utf-8", xml_declaration=True)
    logging.info("✅ SUMO configuration file successfully created.")

if __name__ == "__main__":
    generate_sumo_config()
