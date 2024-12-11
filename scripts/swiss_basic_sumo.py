"""
Generate SUMO-compatible .nod.xml, .edge.xml, and .con.xml files for a railway network.

This script creates nodes, edges, and connections and converts them into
a .net.xml file using netconvert. It adheres to SUMO's recommended practices.

Author: Onur Deniz
"""

import os
import subprocess
from pyproj import Proj, transform

# Paths
OUTPUT_DIR = r"D:/PhD/codingPractices/progress-report-dec-2024/outputs/sumo/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

NODES_FILE = os.path.join(OUTPUT_DIR, "railway_network.nod.xml")
EDGES_FILE = os.path.join(OUTPUT_DIR, "railway_network.edge.xml")
CONNECTIONS_FILE = os.path.join(OUTPUT_DIR, "railway_network.con.xml")
NET_FILE = os.path.join(OUTPUT_DIR, "railway_network.net.xml")
CONFIG_FILE = os.path.join(OUTPUT_DIR, "sumo_config.sumocfg")

# Selected Stations and Lines
STATIONS = [
    {"id": "BS", "name": "Basel SBB", "lat": 47.547, "lon": 7.589},
    {"id": "LST", "name": "Liestal", "lat": 47.486, "lon": 7.734},
    {"id": "SIS", "name": "Sissach", "lat": 47.462, "lon": 7.810},
    {"id": "GKD", "name": "Gelterkinden", "lat": 47.463, "lon": 7.857},
    {"id": "OL", "name": "Olten", "lat": 47.352, "lon": 7.903},
    {"id": "ZF", "name": "Zofingen", "lat": 47.287, "lon": 7.946},
    {"id": "SS", "name": "Sursee", "lat": 47.171, "lon": 8.100},
    {"id": "LZ", "name": "Luzern", "lat": 47.049, "lon": 8.308},
    {"id": "RK", "name": "Rotkreuz", "lat": 47.141, "lon": 8.431},
    {"id": "BAA", "name": "Baar", "lat": 47.195, "lon": 8.532},
    {"id": "TW", "name": "Thalwil", "lat": 47.292, "lon": 8.563},
    {"id": "ZLST", "name": "Zürich Langstrasse", "lat": 47.378, "lon": 8.527},
]

LINES = {
    "500": [
        ("BS", "LST"),
        ("LST", "SIS"),
        ("SIS", "GKD"),
        ("GKD", "OL"),
        ("OL", "ZF"),
        ("ZF", "SS"),
        ("SS", "LZ"),
    ],
    "660": [("LZ", "RK")],
    "720": [
        ("RK", "BAA"),
        ("BAA", "TW"),
        ("TW", "ZLST"),
    ],
}

# Initialize Proj
proj_wgs84 = Proj(init="epsg:4326")  # WGS84 Latitude/Longitude
proj_utm = Proj(init="epsg:32632")  # UTM Zone 32N (covers Switzerland)

def latlon_to_cartesian(lat, lon):
    """
    Converts latitude and longitude to Cartesian coordinates (UTM).
    """
    x, y = transform(proj_wgs84, proj_utm, lon, lat)
    return x, y


def create_nodes_file():
    """
    Creates the SUMO nodes file (.nod.xml).
    """
    with open(NODES_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<nodes>\n")
        for station in STATIONS:
            x, y = latlon_to_cartesian(station["lat"], station["lon"])
            f.write(f'  <node id="{station["id"]}" x="{x}" y="{y}" type="railSignal"/>\n')
        f.write("</nodes>\n")
    print(f"Nodes file created at: {NODES_FILE}")


def create_edges_file():
    """
    Creates the SUMO edges file (.edge.xml).
    """
    with open(EDGES_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<edges>\n")
        for line_id, segments in LINES.items():
            for start, end in segments:
                f.write(
                    f'  <edge id="{line_id}_{start}_{end}" from="{start}" to="{end}" priority="1" numLanes="1" speed="30"/>\n'
                )
        f.write("</edges>\n")
    print(f"Edges file created at: {EDGES_FILE}")


def create_connections_file():
    """
    Creates the SUMO connections file (.con.xml).
    """
    with open(CONNECTIONS_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<connections>\n")
        for line_id, segments in LINES.items():
            for i in range(len(segments) - 1):
                from_edge = f"{line_id}_{segments[i][0]}_{segments[i][1]}"
                to_edge = f"{line_id}_{segments[i+1][0]}_{segments[i+1][1]}"
                f.write(
                    f'  <connection from="{from_edge}" to="{to_edge}" fromLane="0" toLane="0"/>\n'
                )
        f.write("</connections>\n")
    print(f"Connections file created at: {CONNECTIONS_FILE}")


def create_network_file():
    """
    Converts .nod.xml, .edge.xml, and .con.xml files into .net.xml using netconvert.
    """
    command = [
        "netconvert",
        "--node-files", NODES_FILE,
        "--edge-files", EDGES_FILE,
        "--connection-files", CONNECTIONS_FILE,
        "--output-file", NET_FILE,
        "--no-internal-links",  # Avoid unnecessary internal edges
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Network file created at: {NET_FILE}")
    except subprocess.CalledProcessError as e:
        print("Error occurred while running netconvert:")
        print(e)


def create_config_file():
    """
    Creates the SUMO configuration file (.sumocfg).
    """
    with open(CONFIG_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write("<configuration>\n")
        f.write("  <input>\n")
        f.write(f'    <net-file value="{os.path.basename(NET_FILE)}"/>\n')
        f.write("  </input>\n")
        f.write("</configuration>\n")
    print(f"Configuration file created at: {CONFIG_FILE}")


def main():
    """
    Main function to generate SUMO network, nodes, edges, connections, and configuration files.
    """
    create_nodes_file()
    create_edges_file()
    create_connections_file()
    create_network_file()
    create_config_file()


if __name__ == "__main__":
    main()
