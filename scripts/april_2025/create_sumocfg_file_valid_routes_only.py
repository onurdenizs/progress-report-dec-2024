import os
import logging
import xml.etree.ElementTree as ET

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    # Define directories
    route_dir = "D:/PhD/codingPractices/progress-report-dec-2024/data/processed/routes/mapped_rou"
    output_cfg_path = "D:/PhD/codingPractices/progress-report-dec-2024/sumo/inputs/april_2025_swiss/april_2025_swiss_mapped_valid_kpis.sumocfg"
    net_path = "D:/PhD/codingPractices/progress-report-dec-2024/sumo/inputs/april_2025_swiss/april_2025_swiss.net.xml"
    vehicle_type_path = "D:/PhD/codingPractices/progress-report-dec-2024/data/processed/routes/vehicle_types.veh.xml"

    # Find .rou.xml files
    route_files = sorted([
        os.path.join(route_dir, f)
        for f in os.listdir(route_dir)
        if f.endswith(".rou.xml") and "91-29" not in f
    ])

    if not route_files:
        logging.warning("No valid route files found.")
        return

    logging.info(f"✅ Found {len(route_files)} valid route files.")

    # Build XML tree
    config = ET.Element("configuration")

    # Input
    input_elem = ET.SubElement(config, "input")
    ET.SubElement(input_elem, "net-file", value=net_path)
    ET.SubElement(input_elem, "route-files", value=",".join(route_files))
    ET.SubElement(input_elem, "additional-files", value=vehicle_type_path)

    # Time
    time_elem = ET.SubElement(config, "time")
    ET.SubElement(time_elem, "begin", value="0")
    ET.SubElement(time_elem, "end", value="3600")

    # Output (tripinfo only for now)
    output_elem = ET.SubElement(config, "output")
    ET.SubElement(output_elem, "tripinfo-output", value="D:/PhD/codingPractices/progress-report-dec-2024/outputs/sumo/tripinfo.xml")

    # Save config
    tree = ET.ElementTree(config)
    tree.write(output_cfg_path, encoding="utf-8", xml_declaration=True)
    logging.info(f"✅ SUMO config successfully saved to: {output_cfg_path}")

if __name__ == "__main__":
    main()
