import random
import logging
import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Input and output file paths
LINIENR_CSV_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\swiss_linienr_stations.csv"
NETWORK_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.net.xml"
OUTPUT_ROUTE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.rou.xml"

# Configurable settings
DEFAULT_WAITING_STATIONS = ["LST", "SIS", "GKD", "OL", "ZF", "SS"]
DEFAULT_WAIT_TIME_RANGE = (60, 180)  # Random wait time in seconds
DEFAULT_SPEED_RANGE = (50, 210)  # Speed range in km/h
MIN_DEPART_TIME = 30  # Minimum departure time in seconds
MAX_DEPART_TIME = 1000  # Maximum departure time in seconds
MIN_DEPART_GAP = 60  # Minimum gap between train departures in seconds

# Constants for SUMO elements
DEFAULT_VEHICLE_TYPE = {
    "id": "defaultTrain",
    "accel": "1.0",
    "decel": "2.5",
    "length": "50",
    "maxSpeed": "70",
    "vClass": "rail"
}


def prettify_xml(elem):
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def load_linenr_stations(linenr_csv_file, linenr):
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


def parse_network_file(network_file):
    edge_map = {}
    lane_map = {}
    ordered_edges = []
    try:
        tree = ET.parse(network_file)
        root = tree.getroot()

        for edge in root.findall("edge"):
            edge_id = edge.get("id")
            if edge_id:
                ordered_edges.append(edge_id)

                for lane in edge.findall("lane"):
                    lane_id = lane.get("id")
                    lane_map.setdefault(edge_id, []).append(lane_id)

                parts = edge_id.split("_")
                if len(parts) >= 3:
                    station_pair = (parts[0][1:], parts[1])
                    edge_map.setdefault(station_pair, []).append(edge_id)

        logger.info(f"Parsed and sorted {len(edge_map)} station pairs from network file.")
        return edge_map, lane_map, ordered_edges

    except Exception as e:
        logger.error(f"Error parsing network file: {e}")
        raise


def generate_vehicle_type(root, vehicle_type):
    ET.SubElement(root, "vType", attrib=vehicle_type)


def generate_route_edges(stations, edge_map, ordered_edges):
    route_edges = []
    for i in range(len(stations) - 1):
        station1 = stations[i]
        station2 = stations[i + 1]
        edges = edge_map.get((station1, station2), [])
        route_edges.extend(edges)
    route_edges = [edge for edge in ordered_edges if edge in route_edges]
    return route_edges


def generate_routes_with_stops(linenr, stations, edge_map, lane_map, ordered_edges, waiting_stations, wait_time_range, speed_range, min_depart_time, max_depart_time, min_depart_gap, output_file):
    root = ET.Element("routes")

    # Add default vehicle type
    generate_vehicle_type(root, DEFAULT_VEHICLE_TYPE)

    route_edges = generate_route_edges(stations, edge_map, ordered_edges)

    # Define shared route
    route_id = f"route_linenr_{linenr}"
    ET.SubElement(root, "route", id=route_id, edges=" ".join(route_edges))

    depart_times = []
    for train_num in range(1, 6):
        min_speed, max_speed = speed_range
        speed = round(random.uniform(min_speed, max_speed) / 3.6, 2)

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

        if len(depart_times) < train_num:
            logger.warning(f"Skipping train {train_num} due to departure time constraints.")
            continue

        vehicle_elem = ET.SubElement(root, "vehicle", id=f"train_{linenr}_{train_num}", type="defaultTrain", route=route_id, depart=str(depart_time), speed=str(speed))

        for stop_station in waiting_stations:
            if stop_station in stations:
                stop_idx = stations.index(stop_station)
                if stop_idx > 0:
                    station1 = stations[stop_idx - 1]
                    station2 = stop_station
                    stop_edge = edge_map.get((station1, station2), [])[-1]
                    lanes = lane_map.get(stop_edge, [])
                    if stop_edge and lanes:
                        min_wait, max_wait = wait_time_range
                        duration = random.randint(min_wait, max_wait)
                        ET.SubElement(vehicle_elem, "stop", edge=stop_edge, duration=str(duration))

    try:
        prettified_xml = prettify_xml(root)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prettified_xml)
        logger.info(f"Route file created: {output_file}")
    except IOError as e:
        logger.error(f"Failed to write route file: {e}")
        raise


def main():
    linenr = 500
    logger.info(f"Processing routes for linienr {linenr}...")

    stations = load_linenr_stations(LINIENR_CSV_FILE, linenr)
    edge_map, lane_map, ordered_edges = parse_network_file(NETWORK_FILE)

    generate_routes_with_stops(
        linenr,
        stations,
        edge_map,
        lane_map,
        ordered_edges,
        DEFAULT_WAITING_STATIONS,
        DEFAULT_WAIT_TIME_RANGE,
        DEFAULT_SPEED_RANGE,
        MIN_DEPART_TIME,
        MAX_DEPART_TIME,
        MIN_DEPART_GAP,
        OUTPUT_ROUTE_FILE
    )

    logger.info("Route generation and validation completed successfully.")


if __name__ == "__main__":
    main()
