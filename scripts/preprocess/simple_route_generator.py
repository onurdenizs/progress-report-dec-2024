import random
import logging
import xml.etree.ElementTree as ET
from xml.dom import minidom

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# File paths
OUTPUT_ROUTE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_compV2.rou.xml"

# Configuration
EDGE_LIST = [
    'edge_BSO_BSNO', 'edge_BSNO_GELW', 'edge_GELW_MU', 'edge_MU_MUOS', 'edge_MUOS_PRW',
    'edge_PRW_PRUW', 'edge_PRUW_PR', 'edge_PRO_FRE', 'edge_LSTN_LST', 'edge_LST_LSN',
    'edge_SIS_DIE', 'edge_OLN_OL', 'edge_OL_OLS', 'edge_OLS_ABO', 'edge_ABO_ABOS',
    'edge_ABOS_ZFN', 'edge_ZFN_ZF', 'edge_SSST_SS', 'edge_HUEB_GSAG', 'edge_FMUE_GTS',
    'edge_GTS_HEIM', 'edge_LZEF_LZ'
]
DEFAULT_WAITING_STATIONS = ["LST", "SIS", "OL", "ZFN", "SSST"]  # Stations where trains wait
DEFAULT_WAIT_TIME_RANGE = (60, 180)  # Random wait time in seconds
DEFAULT_SPEED_RANGE = (50, 200)  # Speed range in km/h
DEPARTURE_TIME_RANGE = (30, 4800)  # Random departure time range in seconds
MIN_DEPARTURE_GAP = 120  # Minimum gap between departures
NUM_TRAINS = 15  # Number of trains

DEFAULT_VEHICLE_TYPE = {
    "id": "defaultTrain",
    "accel": "1.0",
    "decel": "2.5",
    "length": "50",
    "maxSpeed": "70",
    "vClass": "rail"
}

def prettify_xml(elem):
    """Prettify XML for better readability."""
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def generate_vehicle_type(root, vehicle_type):
    """Define vehicle type in the XML."""
    ET.SubElement(root, "vType", attrib=vehicle_type)

def generate_departure_times(num_trains, departure_time_range, min_depart_gap):
    """
    Generate departure times for trains, ensuring they respect the minimum gap.

    Args:
        num_trains (int): Number of trains.
        departure_time_range (tuple): Tuple with (min_depart, max_depart) range.
        min_depart_gap (int): Minimum gap between consecutive trains.

    Returns:
        list: List of departure times (integers).
    """
    min_depart, max_depart = departure_time_range
    # Generate random departure times
    depart_times = sorted(random.uniform(min_depart, max_depart) for _ in range(num_trains))
    
    # Adjust times to respect minimum gap
    for i in range(1, len(depart_times)):
        if depart_times[i] - depart_times[i - 1] < min_depart_gap:
            depart_times[i] = depart_times[i - 1] + min_depart_gap
    
    # Ensure times are within the max_depart limit
    depart_times = [int(time) for time in depart_times if time <= max_depart]
    return depart_times

def generate_routes_and_vehicles(output_file, edges, waiting_stations, wait_time_range, speed_range, departure_time_range, min_depart_gap, num_trains):
    """Generate routes and vehicles with random parameters."""
    root = ET.Element("routes")

    # Add default vehicle type
    generate_vehicle_type(root, DEFAULT_VEHICLE_TYPE)

    # Create the route
    route_id = "randomized_route"
    ET.SubElement(root, "route", id=route_id, edges=" ".join(edges))

    # Generate departure times
    depart_times = generate_departure_times(num_trains, departure_time_range, min_depart_gap)

    # Generate vehicles
    for train_num, depart_time in enumerate(depart_times, start=1):
        # Random max speed
        min_speed, max_speed = speed_range
        max_speed_kmh = random.uniform(min_speed, max_speed)
        max_speed_mps = round(max_speed_kmh / 3.6, 2)

        vehicle_elem = ET.SubElement(root, "vehicle", id=f"train_{train_num}", type="defaultTrain", route=route_id, depart=str(depart_time), maxSpeed=str(max_speed_mps))

        # Add stops at specified stations
        for stop_station in waiting_stations:
            stop_edge_candidates = [edge for edge in edges if stop_station in edge]
            if stop_edge_candidates:
                stop_edge = random.choice(stop_edge_candidates)
                wait_time = random.randint(*wait_time_range)
                ET.SubElement(vehicle_elem, "stop", edge=stop_edge, duration=str(wait_time))

    # Write to output file
    try:
        prettified_xml = prettify_xml(root)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prettified_xml)
        logger.info(f"Route file created: {output_file}")
    except IOError as e:
        logger.error(f"Failed to write route file: {e}")
        raise

def main():
    logger.info("Generating routes and vehicles with randomized parameters...")
    generate_routes_and_vehicles(
        output_file=OUTPUT_ROUTE_FILE,
        edges=EDGE_LIST,
        waiting_stations=DEFAULT_WAITING_STATIONS,
        wait_time_range=DEFAULT_WAIT_TIME_RANGE,
        speed_range=DEFAULT_SPEED_RANGE,
        departure_time_range=DEPARTURE_TIME_RANGE,
        min_depart_gap=MIN_DEPARTURE_GAP,
        num_trains=NUM_TRAINS
    )
    logger.info("Route generation completed.")

if __name__ == "__main__":
    main()
