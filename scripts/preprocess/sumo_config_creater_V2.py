import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Paths
NETWORK_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_compV2.net.xml"
ROUTE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_compV2.rou.xml"
OUTPUT_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\outputs\sw_real_comp"
OUTPUT_PREFIX = "sw_comp_output"
CONFIG_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_compV2.sumocfg"

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def prettify_xml(elem):
    """Prettifies XML string output."""
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def get_last_departure_time(route_file):
    """
    Parses the route file to find the last train's departure time.

    Args:
        route_file (str): Path to the SUMO route file.

    Returns:
        int: The last train's departure time in seconds.
    """
    try:
        tree = ET.parse(route_file)
        root = tree.getroot()

        max_depart_time = 0
        for vehicle in root.findall("vehicle"):
            depart_time = float(vehicle.get("depart", 0))
            max_depart_time = max(max_depart_time, depart_time)

        return int(max_depart_time)
    except Exception as e:
        print(f"Error reading route file {route_file}: {e}")
        raise

def create_sumo_config_file(network_file, route_file, output_dir, output_prefix, config_file):
    """
    Creates a SUMO configuration file for the simulation.

    Args:
        network_file (str): Path to the network file.
        route_file (str): Path to the route file.
        output_dir (str): Directory for output files.
        output_prefix (str): Prefix for output files.
        config_file (str): Path to save the configuration file.
    """
    root = ET.Element("configuration")

    # Input section
    input_elem = ET.SubElement(root, "input")
    ET.SubElement(input_elem, "net-file", value=network_file)
    ET.SubElement(input_elem, "route-files", value=route_file)

    # Output section
    output_elem = ET.SubElement(root, "output")
    ET.SubElement(output_elem, "fcd-output", value=os.path.join(output_dir, f"{output_prefix}_fcd.xml"))
    ET.SubElement(output_elem, "tripinfo-output", value=os.path.join(output_dir, f"{output_prefix}_tripinfo.xml"))
    ET.SubElement(output_elem, "emission-output", value=os.path.join(output_dir, f"{output_prefix}_emissions.xml"))
    ET.SubElement(output_elem, "full-output", value=os.path.join(output_dir, f"{output_prefix}_full.xml"))

    # Time section
    time_elem = ET.SubElement(root, "time")
    begin_time = 0
    last_departure_time = get_last_departure_time(route_file)
    end_time = last_departure_time + 3600  # Add 1 hour to the last departure time
    ET.SubElement(time_elem, "begin", value=str(begin_time))
    ET.SubElement(time_elem, "end", value=str(end_time))

    # Save the configuration file
    try:
        config_content = prettify_xml(root)
        with open(config_file, "w", encoding="utf-8") as file:
            file.write(config_content)
        print(f"SUMO configuration file created: {config_file}")
    except IOError as e:
        print(f"Error writing SUMO configuration file: {e}")

# Generate the configuration file
create_sumo_config_file(NETWORK_FILE, ROUTE_FILE, OUTPUT_DIR, OUTPUT_PREFIX, CONFIG_FILE)
