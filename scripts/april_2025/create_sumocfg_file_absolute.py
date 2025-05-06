"""
create_sumocfg_file_absolute.py

Generates a SUMO config (.sumocfg) using absolute paths for reliable GUI launching.
Author: GPT-4 + Onur | April 2025
"""

import os
import xml.etree.ElementTree as ET
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# -------------------------
# Absolute Paths
# -------------------------
CONFIG_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\april_2025_swiss\april_2025_swiss.sumocfg"
NET_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\april_2025_swiss\april_2025_swiss.net.xml"
ROUTE_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\selected_intercity_routes_with_types.rou.xml"
VEHICLE_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\vehicle_types.veh.xml"
TRIPINFO_OUT = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\outputs\april_2025_swiss\tripinfo.xml"
STOPINFO_OUT = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\outputs\april_2025_swiss\stopinfo.xml"

def generate_absolute_sumocfg(output_path):
    logging.info("🛠️ Generating absolute-path SUMO config...")

    root = ET.Element("configuration")

    input_ = ET.SubElement(root, "input")
    ET.SubElement(input_, "net-file", value=NET_PATH)
    ET.SubElement(input_, "route-files", value=ROUTE_PATH)
    ET.SubElement(input_, "additional-files", value=VEHICLE_PATH)

    output = ET.SubElement(root, "output")
    ET.SubElement(output, "tripinfo-output", value=TRIPINFO_OUT)
    ET.SubElement(output, "stop-output", value=STOPINFO_OUT)

    time = ET.SubElement(root, "time")
    ET.SubElement(time, "begin", value="0")
    ET.SubElement(time, "end", value="36000")  # Simulate 10 hours

    report = ET.SubElement(root, "report")
    ET.SubElement(report, "verbose", value="true")
    ET.SubElement(report, "no-step-log", value="true")

    tree = ET.ElementTree(root)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    logging.info(f"✅ Absolute-path SUMO config saved to: {output_path}")


if __name__ == "__main__":
    generate_absolute_sumocfg(CONFIG_PATH)
