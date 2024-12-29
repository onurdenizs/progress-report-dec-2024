import os
import json
import random
import pandas as pd
from pyproj import Proj, Transformer
from shapely.geometry import LineString
import matplotlib.pyplot as plt

# Define constants
INPUT_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon.geojson"
OUTPUT_DIR = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_samp"
NODE_FILE = os.path.join(OUTPUT_DIR, "sw_real_samp.nod.xml")
EDGE_FILE = os.path.join(OUTPUT_DIR, "sw_real_samp.edge.xml")
CONNECTION_FILE = os.path.join(OUTPUT_DIR, "sw_real_samp.con.xml")
ROUTE_FILE = os.path.join(OUTPUT_DIR, "sw_real_samp.rou.xml")
NET_FILE = os.path.join(OUTPUT_DIR, "sw_real_samp.net.xml")
SUMO_CONFIG_FILE = os.path.join(OUTPUT_DIR, "sw_real_samp.sumocfg")

# Coordinate systems
WGS84 = "epsg:4326"  # Input coordinate system
UTM = "epsg:32633"   # UTM zone for Switzerland
transformer = Transformer.from_crs(WGS84, UTM, always_xy=True)

# Create output directory if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def convert_to_utm(coords):
    """Convert WGS84 coordinates to UTM.

    Args:
        coords (list): List of [longitude, latitude] pairs.

    Returns:
        list: Converted coordinates in UTM.
    """
    return [transformer.transform(lon, lat) for lon, lat in coords]

def process_geojson(input_file):
    """Load and preprocess GeoJSON data.

    Args:
        input_file (str): Path to the input GeoJSON file.

    Returns:
        pd.DataFrame: Preprocessed data as a pandas DataFrame.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    records = [
        {
            "geometry": feature["geometry"],
            **feature["properties"]
        }
        for feature in data["features"]
    ]
    return pd.DataFrame(records)

def filter_segments(df, linienr, segments):
    """Filter segments for a specific line number and sub-segments.

    Args:
        df (pd.DataFrame): Input DataFrame.
        linienr (int): Line number.
        segments (list): List of [start_op, end_op] pairs.

    Returns:
        list: List of shapely LineString objects.
    """
    filtered = df[(df["linienr"] == linienr) & 
                  df[["bp_anfang", "bp_ende"]].apply(tuple, axis=1).isin(segments)]
    filtered = filtered.sort_values(by="km_agm_von")
    return [
        LineString(convert_to_utm(geometry["coordinates"]))
        for geometry in filtered["geometry"]
    ]

def create_stations():
    """Create XML nodes for stations.

    Returns:
        dict: Dictionary of station node IDs and shifted UTM coordinates.
    """
    stations = {
        "BS": (7.589, 47.548), "LZ": (8.309, 47.050), "LST": (7.733, 47.482),
        "SIS": (7.816, 47.462), "GKD": (7.867, 47.457), "OL": (7.917, 47.351),
        "ZF": (7.947, 47.282), "SS": (8.096, 47.172), "RK": (8.356, 47.045),
        "ZG": (8.524, 47.177), "BAA": (8.626, 47.202), "TW": (8.697, 47.256),
        "ZLST": (8.539, 47.378), "LZEF": (8.299, 47.051), "FMUE": (8.296, 47.052),
        "ROTS": (8.295, 47.053), "TWNO": (8.700, 47.255), "ZLOG": (8.710, 47.258)
    }

    utm_stations = {station: convert_to_utm([coords])[0] for station, coords in stations.items()}

    x_coords = [utm[0] for utm in utm_stations.values()]
    y_coords = [utm[1] for utm in utm_stations.values()]
    shift_x = min(x_coords)
    shift_y = min(y_coords)

    shifted_stations = {
        station: (utm[0] - shift_x, utm[1] - shift_y)
        for station, utm in utm_stations.items()
    }
    return shifted_stations

def generate_station_nodes(stations):
    """Generate XML nodes for stations.

    Args:
        stations (dict): Dictionary of station IDs and shifted coordinates.

    Returns:
        list: List of station node XML strings.
    """
    return [
        f'<node id="{station}" x="{utm[0]}" y="{utm[1]}" />'
        for station, utm in stations.items()
    ]

def visualize_network(stations):
    """Visualize the station positions to verify coordinates.

    Args:
        stations (dict): Dictionary of station IDs and coordinates.
    """
    x_coords = [utm[0] for utm in stations.values()]
    y_coords = [utm[1] for utm in stations.values()]

    plt.figure(figsize=(10, 6))
    plt.scatter(x_coords, y_coords, c="blue", marker="o")
    for station, (x, y) in stations.items():
        plt.text(x, y, station, fontsize=8, ha="right")
    plt.title("Station Positions (Shifted Coordinates)")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.grid(True)
    plt.show()

def main():
    """Main function to execute the script."""
    print("Loading dataset...")
    df = process_geojson(INPUT_FILE)

    print("Creating stations...")
    shifted_stations = create_stations()
    stations_xml = generate_station_nodes(shifted_stations)
    print(f"{len(stations_xml)} stations created.")

    print("Visualizing stations...")
    visualize_network(shifted_stations)

    print("Generating XML files...")
    # Write nodes
    with open(NODE_FILE, "w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<nodes>\n')
        f.write("\n".join(stations_xml))
        f.write("\n</nodes>")
    print(f"Node file created: {NODE_FILE}")

    print("Running netconvert...")
    command = (
        f"netconvert --node-files={NODE_FILE} --edge-files={EDGE_FILE} "
        f"--connection-files={CONNECTION_FILE} --output-file={NET_FILE}"
    )
    os.system(command)
    print(f"Network file created: {NET_FILE}")

if __name__ == "__main__":
    main()
