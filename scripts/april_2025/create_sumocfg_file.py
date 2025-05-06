"""
create_sumocfg_file.py

Generates a SUMO configuration file (.sumocfg) for the Swiss intercity simulation.
Correctly uses:
- selected_intercity_routes_with_types.rou.xml
- vehicle_types.veh.xml

Outputs config to:
D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\april_2025_swiss\april_2025_swiss.sumocfg

Author: GPT-4 + Onur | April 2025
"""

import os
import xml.etree.ElementTree as ET
import logging

# -------------------------
# Paths
# -------------------------

OUTPUT_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\april_2025_swiss\april_2025_swiss.sumocfg"

ROUTE_PATH = r"..\..\data\processed\routes\selected_intercity_routes_with_types.rou.xml"
VEHICLE_PATH = r"..\..\data\processed\routes\vehicle_types.veh.xml"
TRIPINFO_OUT = r"..\..\outputs\april_2025_swiss\tripinfo.xml"
STOPINFO_OUT = r"..\..\outputs\april_2025_swiss\stopinfo.xml"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def generate_sumocfg(output_path):
    logging.info("🛠️ Generating corrected SUMO config file...")

    root = ET.Element("configuration")

    # Input section
    input_ = ET.SubElement(root, "input")
    ET.SubElement(input_, "net-file", value="april_2025_swiss.net.xml")
    ET.SubElement(input_, "route-files", value=ROUTE_PATH)
    ET.SubElement(input_, "additional-files", value=VEHICLE_PATH)

    # Output section
    output = ET.SubElement(root, "output")
    ET.SubElement(output, "tripinfo-output", value=TRIPINFO_OUT)
    ET.SubElement(output, "stop-output", value=STOPINFO_OUT)

    # Time settings
    time = ET.SubElement(root, "time")
    ET.SubElement(time, "begin", value="0")
    ET.SubElement(time, "end", value="36000")  # 10 hours simulated time

    # Reporting settings
    report = ET.SubElement(root, "report")
    ET.SubElement(report, "verbose", value="true")
    ET.SubElement(report, "no-step-log", value="true")

    # Write to file
    tree = ET.ElementTree(root)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)

    logging.info(f"✅ Corrected SUMO config saved to: {output_path}")


if __name__ == "__main__":
    generate_sumocfg(OUTPUT_PATH)
