"""
regenerate_vehicle_types_ic_ir_only.py

Regenerates vehicle_types.veh.xml with known IDs (IC, IR)
for mapped route simulation.

Author: GPT-4 + Onur | April 2025
"""

import os
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

OUTPUT_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes"
VEHICLE_FILE = os.path.join(OUTPUT_PATH, "vehicle_types.veh.xml")

def main():
    logging.info("🚄 Regenerating vehicle_types.veh.xml with IC and IR...")

    vehicle_types = {
        "IC": {"accel": "1.0", "decel": "1.0", "sigma": "0.5", "length": "200", "minGap": "3.0", "maxSpeed": "55.56"},  # 200 km/h
        "IR": {"accel": "1.0", "decel": "1.0", "sigma": "0.5", "length": "150", "minGap": "3.0", "maxSpeed": "44.44"},  # 160 km/h
    }

    root = ET.Element("additional")
    for vtype_id, attrs in vehicle_types.items():
        ET.SubElement(root, "vType", id=vtype_id, **attrs)

    tree = ET.ElementTree(root)
    tree.write(VEHICLE_FILE, encoding="utf-8", xml_declaration=True)

    logging.info(f"✅ Saved: {VEHICLE_FILE}")

if __name__ == "__main__":
    main()
