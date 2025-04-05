import os
import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# File paths
ROUTE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.rou.xml"
CONFIG_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.sumocfg"
NETWORK_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.net.xml"

OUTPUT_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\outputs\sw_real_comp"
OUTPUT_PREFIX = "sw_comp_output"


# Default simulation settings
EXTRA_SIMULATION_TIME = 3600  # Seconds to add after the last vehicle departs


def prettify_xml(elem):
    """
    Prettify XML for human-readable formatting.

    Args:
        elem (xml.etree.ElementTree.Element): Root XML element.

    Returns:
        str: Prettified XML as a string.
    """
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def get_last_depart_time(route_file):
    """
    Read the route file and find the last departure time.

    Args:
        route_file (str): Path to the route file.

    Returns:
        int: Last departure time in seconds.
    """
    try:
        tree = ET.parse(route_file)
        root = tree.getroot()
        max_depart_time = 0
        for vehicle in root.findall("vehicle"):
            depart_time = int(float(vehicle.get("depart", 0)))
            max_depart_time = max(max_depart_time, depart_time)
        logger.info(f"Last departure time in route file: {max_depart_time}s")
        return max_depart_time
    except Exception as e:
        logger.error(f"Error reading route file: {e}")
        raise


def create_sumo_config(config_file, network_file, route_file, output_dir, output_prefix, simulation_end_time):
    """
    Create a SUMO configuration file.

    Args:
        config_file (str): Path to the SUMO configuration file to create.
        network_file (str): Path to the network file.
        route_file (str): Path to the route file.
        output_dir (str): Directory for output files.
        output_prefix (str): Prefix for output file names.
        simulation_end_time (int): Simulation end time in seconds.
    """
    try:
        root = ET.Element("configuration")

        # Input section
        input_elem = ET.SubElement(root, "input")
        ET.SubElement(input_elem, "net-file", value=network_file)
        ET.SubElement(input_elem, "route-files", value=route_file)

        # Time section
        time_elem = ET.SubElement(root, "time")
        ET.SubElement(time_elem, "begin", value="0")
        ET.SubElement(time_elem, "end", value=str(simulation_end_time))

        # Output section
        output_elem = ET.SubElement(root, "output")
        ET.SubElement(output_elem, "tripinfo-output", value=os.path.join(output_dir, f"{output_prefix}.tripinfo.xml"))
        ET.SubElement(output_elem, "emission-output", value=os.path.join(output_dir, f"{output_prefix}.emissions.xml"))
        ET.SubElement(output_elem, "fcd-output", value=os.path.join(output_dir, f"{output_prefix}.fcd.xml"))
        ET.SubElement(output_elem, "edgedata-output", value=os.path.join(output_dir, f"{output_prefix}.edg.xml"))

        # Write prettified XML to config file
        prettified_xml = prettify_xml(root)
        with open(config_file, "w", encoding="utf-8") as f:
            f.write(prettified_xml)
        logger.info(f"SUMO configuration file created: {config_file}")
    except Exception as e:
        logger.error(f"Error creating SUMO configuration file: {e}")
        raise


def main():
    """
    Main function to create the SUMO configuration file.
    """
    try:
        # Get the last departure time from the route file
        last_depart_time = get_last_depart_time(ROUTE_FILE)

        # Calculate simulation end time
        simulation_end_time = last_depart_time + EXTRA_SIMULATION_TIME

        # Create the configuration file
        create_sumo_config(CONFIG_FILE, NETWORK_FILE, ROUTE_FILE, OUTPUT_DIR, OUTPUT_PREFIX, simulation_end_time)

        logger.info("SUMO configuration generation completed successfully.")
    except Exception as e:
        logger.error(f"Failed to generate SUMO configuration: {e}")
        raise


if __name__ == "__main__":
    main()
