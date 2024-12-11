import os
import geopandas as gpd
import pandas as pd
from pyproj import Proj, transform
import subprocess

# Paths for output files
OUTPUT_DIR = r"D:/PhD/codingPractices/progress-report-dec-2024/outputs/sumo/french/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NODES_FILE = os.path.join(OUTPUT_DIR, "french_network.nod.xml")
EDGES_FILE = os.path.join(OUTPUT_DIR, "french_network.edge.xml")
CONNECTIONS_FILE = os.path.join(OUTPUT_DIR, "french_network.con.xml")
NET_FILE = os.path.join(OUTPUT_DIR, "french_network.net.xml")
ROUTE_FILE = os.path.join(OUTPUT_DIR, "french_routes.rou.xml")
CONFIG_FILE = os.path.join(OUTPUT_DIR, "sumo_config.sumocfg")

VITESSE_PATH = r"D:/PhD/codingPractices/progress-report-dec-2024/data/raw/french/vitesse_maximale/vitesse_maximale.geojson"

STATIONS = [
    {"id": "PLE", "name": "Paris L'est", "lat": 48.876, "lon": 2.358},
    {"id": "BFT", "name": "Belfort", "lat": 47.637, "lon": 6.864},
    {"id": "MLS", "name": "Mulhouse", "lat": 47.748, "lon": 7.339},
    {"id": "PM", "name": "Paris-Montparnasse", "lat": 48.839, "lon": 2.320},
    {"id": "RNS", "name": "Rennes", "lat": 48.108, "lon": -1.677},
    {"id": "BST", "name": "Brest", "lat": 48.390, "lon": -4.486},
    {"id": "PTL", "name": "Paris gare de Lyon", "lat": 48.844, "lon": 2.374},
    {"id": "AVN", "name": "Avignon", "lat": 43.948, "lon": 4.807},
    {"id": "MS", "name": "Marseille", "lat": 43.297, "lon": 5.381},
]

LINES = {
    "001000": [("PLE", "BFT"), ("BFT", "MLS")],
    "420000": [("PM", "RNS"), ("RNS", "BST")],
    "830000": [("PTL", "AVN"), ("AVN", "MS")],
}

# Coordinate systems for projection
proj_wgs84 = Proj(init="epsg:4326")
proj_utm = Proj(init="epsg:32631")

def latlon_to_cartesian(lat, lon):
    """
    Converts latitude and longitude to Cartesian coordinates using UTM projection.

    Args:
        lat (float): Latitude in decimal degrees.
        lon (float): Longitude in decimal degrees.

    Returns:
        tuple: Cartesian coordinates (x, y).
    """
    x, y = transform(proj_wgs84, proj_utm, lon, lat)
    return x, y

def get_segment_speed(line_id, start, end, vitesse_data):
    """
    Retrieves the speed of a segment from the dataset, converting from km/h to m/s.

    Args:
        line_id (str): Line ID of the segment.
        start (str): Start station ID.
        end (str): End station ID.
        vitesse_data (GeoDataFrame): Dataset containing speed information.

    Returns:
        float: Speed in m/s.
    """
    if 'v_max' not in vitesse_data.columns:
        print("Error: 'v_max' column not found in dataset.")
        return 30 / 3.6  # Default speed

    segment = vitesse_data[(vitesse_data["code_ligne"] == line_id)]

    if not segment.empty:
        segment["v_max"] = pd.to_numeric(segment["v_max"], errors="coerce") / 3.6
        return segment["v_max"].max() if not pd.isnull(segment["v_max"].max()) else 30 / 3.6

    return 30 / 3.6

def create_nodes_file():
    """
    Creates the SUMO nodes file based on station data.
    """
    with open(NODES_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<nodes>\n")
        for station in STATIONS:
            x, y = latlon_to_cartesian(station["lat"], station["lon"])
            f.write(f'  <node id="{station["id"]}" x="{x}" y="{y}" type="railSignal"/>\n')
        f.write("</nodes>\n")
    print(f"Nodes file created at: {NODES_FILE}")

def create_edges_file(vitesse_data):
    """
    Creates the SUMO edges file with speed information.

    Args:
        vitesse_data (GeoDataFrame): Dataset containing speed information.
    """
    with open(EDGES_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<edges>\n")
        for line_id, segments in LINES.items():
            for start, end in segments:
                speed = get_segment_speed(line_id, start, end, vitesse_data)
                f.write(
                    f'  <edge id="{line_id}_{start}_{end}" from="{start}" to="{end}" priority="1" numLanes="1" speed="{speed}"/>\n'
                )
        f.write("</edges>\n")
    print(f"Edges file created at: {EDGES_FILE}")

def create_connections_file():
    """
    Creates the SUMO connections file.
    """
    with open(CONNECTIONS_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<connections>\n")
        for line_id, segments in LINES.items():
            for i in range(len(segments) - 1):
                from_edge = f"{line_id}_{segments[i][0]}_{segments[i][1]}"
                to_edge = f"{line_id}_{segments[i + 1][0]}_{segments[i + 1][1]}"
                f.write(f'  <connection from="{from_edge}" to="{to_edge}" fromLane="0" toLane="0"/>\n')
        f.write("</connections>\n")
    print(f"Connections file created at: {CONNECTIONS_FILE}")

def create_network_file():
    """
    Generates the SUMO network file using netconvert.
    """
    command = [
        "netconvert",
        "--node-files", NODES_FILE,
        "--edge-files", EDGES_FILE,
        "--connection-files", CONNECTIONS_FILE,
        "--output-file", NET_FILE,
        "--no-internal-links",
    ]
    subprocess.run(command, check=True)
    print(f"Network file created at: {NET_FILE}")

def create_routes_file():
    """
    Creates the SUMO routes file for vehicle definitions and routes.
    """
    with open(ROUTE_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<routes>\n')
        f.write('<vType id="train1" vClass="rail" maxSpeed="61.11" carFollowModel="Rail"/>\n')
        f.write('<vType id="train2" vClass="rail" maxSpeed="55.55" carFollowModel="Rail"/>\n')
        f.write('<vType id="train3" vClass="rail" maxSpeed="30" carFollowModel="Rail"/>\n')
        f.write('<route id="route1" edges="001000_PLE_BFT 001000_BFT_MLS"/>\n')
        f.write('<route id="route2" edges="420000_PM_RNS 420000_RNS_BST"/>\n')
        f.write('<route id="route3" edges="830000_PTL_AVN 830000_AVN_MS"/>\n')
        f.write('<vehicle id="veh1" type="train1" route="route1" depart="0"/>\n')
        f.write('<vehicle id="veh2" type="train2" route="route2" depart="50"/>\n')
        f.write('<vehicle id="veh3" type="train3" route="route3" depart="100"/>\n')
        f.write('</routes>\n')
    print(f"Routes file created at: {ROUTE_FILE}")

def create_config_file():
    """
    Creates the SUMO configuration file.
    """
    with open(CONFIG_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<configuration>\n")
        f.write("    <input>\n")
        f.write(f'        <net-file value="{os.path.basename(NET_FILE)}"/>\n')
        f.write(f'        <route-files value="{os.path.basename(ROUTE_FILE)}"/>\n')
        f.write("    </input>\n")
        f.write("    <output>\n")
        f.write('        <fcd-output value="D:/PhD/codingPractices/progress-report-dec-2024/outputs/french/french_simulation_output.xml"/>\n')
        f.write("    </output>\n")
        f.write("    <time>\n")
        f.write("        <begin value=\"0\"/>\n")
        f.write("        <end value=\"3600\"/>\n")
        f.write("    </time>\n")
        f.write("</configuration>\n")
    print(f"Configuration file created at: {CONFIG_FILE}")

def main():
    """
    Main function to generate all SUMO input files.
    """
    vitesse_data = gpd.read_file(VITESSE_PATH)
    create_nodes_file()
    create_edges_file(vitesse_data)
    create_connections_file()
    create_network_file()
    create_routes_file()
    create_config_file()

if __name__ == "__main__":
    main()
