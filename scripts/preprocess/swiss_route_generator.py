import random
import os
import logging
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Input and output file paths
LINIENR_CSV_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\swiss_linienr_stations.csv"
OUTPUT_ROUTE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_samp.rou.xml"

# Configurable settings
DEFAULT_WAITING_STATIONS = ["BS", "LST", "SIS", "GKD", "OL", "ZF", "SS", "LZ"]
DEFAULT_WAIT_TIME_RANGE = (60, 180)  # Random wait time in seconds
DEFAULT_SPEED_RANGE = (50, 210)  # Speed range in km/h
MIN_DEPART_TIME = 30  # Minimum departure time in seconds
MAX_DEPART_TIME = 1000  # Maximum departure time in seconds
MIN_DEPART_GAP = 60  # Minimum gap between train departures in seconds

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

def load_linenr_stations(linenr_csv_file, linenr):
    """
    Load station data for a specific linienr from the CSV file.

    Args:
        linenr_csv_file (str): Path to the CSV file containing linienr and stations.
        linenr (int): Linienr for which stations are to be fetched.

    Returns:
        list: Ordered list of stations for the linienr.
    """
    try:
        with open(linenr_csv_file, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if int(row["linienr"]) == linenr:
                    stations = row["stations"].replace('"', "").split(", ")
                    logger.info(f"Stations for linienr {linenr}: {stations}")
                    return stations
    except Exception as e:
        logger.error(f"Error loading linienr stations: {e}")
        raise
    raise ValueError(f"Linienr {linenr} not found in the CSV file.")

def generate_routes(linenr, stations, waiting_stations, wait_time_range, speed_range, min_depart_time, max_depart_time, min_depart_gap, output_file):
    """
    Generate a SUMO route file with specific routes, speeds, stops, waiting times, and departure times.

    Args:
        linenr (int): Linienr for the train.
        stations (list): Ordered list of stations for the route.
        waiting_stations (list): Stations where vehicles stop.
        wait_time_range (tuple): Min and max wait times in seconds.
        speed_range (tuple): Min and max speeds in km/h.
        min_depart_time (int): Earliest possible departure time in seconds.
        max_depart_time (int): Latest possible departure time in seconds.
        min_depart_gap (int): Minimum gap between train departures in seconds.
        output_file (str): Path to the output route file.
    """
    root = ET.Element("routes")

    # Define route ID and edges
    route_id = f"route_linenr_{linenr}"
    route_edges = " ".join(stations)
    ET.SubElement(root, "route", id=route_id, edges=route_edges)

    # Generate vehicles
    depart_times = []
    for train_num in range(1, 6):  # Five trains
        # Generate random speed in m/s
        min_speed, max_speed = speed_range
        speed = round(random.uniform(min_speed, max_speed) / 3.6, 2)  # Convert km/h to m/s

        # Ensure valid departure times with minimum gap
        while True:
            if not depart_times:
                depart_time = random.randint(min_depart_time, max_depart_time)
            else:
                next_depart_start = depart_times[-1] + min_depart_gap
                if next_depart_start > max_depart_time:
                    logger.warning(f"Cannot add train {train_num} due to insufficient departure window.")
                    break
                depart_time = random.randint(next_depart_start, max_depart_time)

            if not depart_times or (depart_time - depart_times[-1]) >= min_depart_gap:
                depart_times.append(depart_time)
                break

        # If no valid depart time could be generated, skip this train
        if len(depart_times) < train_num:
            logger.warning(f"Skipping train {train_num} due to departure time constraints.")
            continue

        # Define the vehicle
        vehicle_elem = ET.SubElement(root, "vehicle", id=f"train_train_{linenr}_{train_num}", route=route_id, depart=str(depart_time), speed=str(speed))

        # Add stops with waiting times at specific stations
        missing_stations = []
        for station in waiting_stations:
            if station in stations:
                min_wait, max_wait = wait_time_range
                duration = random.randint(min_wait, max_wait)  # Random wait time in seconds
                ET.SubElement(vehicle_elem, "stop", edge=station, duration=str(duration))
            else:
                missing_stations.append(station)

        # Log missing stations
        if missing_stations:
            logger.warning(f"The following stations are not part of the route for linienr {linenr}: {missing_stations}")

    # Write prettified XML to output file
    try:
        prettified_xml = prettify_xml(root)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prettified_xml)
        logger.info(f"Route file created: {output_file}")
    except Exception as e:
        logger.error(f"Failed to write route file: {e}")
        raise

def main():
    """
    Main function to generate routes for a specified linienr.
    """
    linenr = 500  # Example linienr
    logger.info(f"Processing routes for linienr {linenr}...")

    # Load stations for the given linienr
    stations = load_linenr_stations(LINIENR_CSV_FILE, linenr)

    # Generate routes with waiting times, speed ranges, and departure times
    generate_routes(
        linenr,
        stations,
        DEFAULT_WAITING_STATIONS,
        DEFAULT_WAIT_TIME_RANGE,
        DEFAULT_SPEED_RANGE,
        MIN_DEPART_TIME,
        MAX_DEPART_TIME,
        MIN_DEPART_GAP,
        OUTPUT_ROUTE_FILE
    )

    logger.info("Route generation completed successfully.")

if __name__ == "__main__":
    main()
