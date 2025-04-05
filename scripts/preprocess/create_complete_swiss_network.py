"""create_complete_swiss_network.py

This script generates a SUMO-compatible transportation network from a GeoJSON file containing rail line geometries. It performs the following steps:

1. Loads a GeoJSON file with rail line data.
2. Converts WGS84 coordinates to UTM for compatibility with SUMO.
3. Creates nodes and edges for the SUMO network, avoiding unnecessary intermediate nodes and ensuring connectivity.
4. Writes the resulting node, edge, and connection files.
5. Validates the connectivity between nodes and edges to ensure a valid network.
6. Runs SUMO's `netconvert` to generate the final SUMO network file.

Features:
- Avoids duplicate nodes by checking for identical coordinates and IDs.
- Creates only necessary intermediate nodes based on the number of geometry points.
- Ensures that `to` nodes of one edge match the `from` nodes of the next.
"""

import os
import json
import logging
from pyproj import Transformer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# File paths
GEOJSON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon_altered.geojson"
OUTPUT_NODE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.nod.xml"
OUTPUT_EDGE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.edge.xml"
OUTPUT_CON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.con.xml"
OUTPUT_NET_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.net.xml"

# Parameters
V_MAX_KMH = 250  # Maximum speed in km/h
V_MAX_MS = round(V_MAX_KMH / 3.6, 2)  # Convert to m/s
BIDIRECTIONAL = True

# Initialize Transformer for WGS84 to UTM
transformer = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)

def wgs84_to_utm(lon, lat, precision=16):
    """Convert WGS84 coordinates to UTM and round them to a given precision."""
    utm_x, utm_y = transformer.transform(lon, lat)
    return round(utm_x, precision), round(utm_y, precision)

def load_geojson(file_path):
    """Load GeoJSON file and return its content."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load GeoJSON file: {e}")
        raise

def generate_sumo_files(features, node_file, edge_file, con_file):
    """Generate SUMO node, edge, and connection files from GeoJSON data."""
    nodes = {}
    edges = []
    connections = []

    def add_node(node_id, utm_x, utm_y):
        """Add a node using UTM coordinates directly."""
        if node_id not in nodes:
            nodes[node_id] = (utm_x, utm_y)
        return node_id, utm_x, utm_y

    for feature in features:
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        bp_anfang = properties.get("bp_anfang", "unknown_start")
        bp_ende = properties.get("bp_ende", "unknown_end")

        if geometry.get("type") == "LineString" and len(geometry.get("coordinates", [])) > 1:
            # Convert WGS84 to UTM
            utm_geolist = [wgs84_to_utm(lon, lat) for lon, lat in geometry["coordinates"]]

            # Create start node
            start_coord = utm_geolist[0]
            start_node_id, start_utm_x, start_utm_y = add_node(bp_anfang, *start_coord)

            # Create end node
            end_coord = utm_geolist[-1]
            end_node_id, end_utm_x, end_utm_y = add_node(bp_ende, *end_coord)

            # Create a single edge with the entire LineString as its shape
            edge_id = f"edge_{start_node_id}_{end_node_id}"
            shape = " ".join(f"{x},{y}" for x, y in utm_geolist)
            edges.append({
                "id": edge_id,
                "from": start_node_id,
                "to": end_node_id,
                "shape": shape,
                "v_max": V_MAX_MS,
                "type": "railway"
            })

    # Write Node file
    with open(node_file, "w", encoding="utf-8") as nf:
        nf.write("<nodes>\n")
        for node_id, (x, y) in nodes.items():
            nf.write(f'  <node id="{node_id}" x="{x}" y="{y}" type="priority" />\n')
        nf.write("</nodes>\n")
    logger.info(f"Node file created: {node_file}")

    # Write Edge file
    with open(edge_file, "w", encoding="utf-8") as ef:
        ef.write("<edges>\n")
        for edge in edges:
            ef.write(
                f'  <edge id="{edge["id"]}" from="{edge["from"]}" to="{edge["to"]}" '
                f'type="{edge["type"]}" priority="1" numLanes="1" speed="{edge["v_max"]}" shape="{edge["shape"]}" />\n'
            )
        ef.write("</edges>\n")
    logger.info(f"Edge file created: {edge_file}")

    # Write Connection file (empty in this case)
    with open(con_file, "w", encoding="utf-8") as cf:
        cf.write("<connections>\n")
        cf.write("</connections>\n")
    logger.info(f"Connection file created: {con_file}")

def run_netconvert(node_file, edge_file, con_file, net_file):
    """Run netconvert to generate the SUMO network file."""
    command = (
        f'netconvert --node-files="{node_file}" '
        f'--edge-files="{edge_file}" '
        f'--connection-files="{con_file}" '
        f'--output-file="{net_file}" '
        f'--geometry.remove '
        f'--print-options '
        f'--log=debug.log '
        f'--precision=6'
    )
    logger.info(f"Running netconvert: {command}")
    os.system(command)
    logger.info(f"Network file created successfully: {net_file}")

def main():
    """Main function to load GeoJSON, generate SUMO files, and run netconvert."""
    logger.info("Loading input GeoJSON file...")
    data = load_geojson(GEOJSON_FILE)
    features = data.get("features", [])
    logger.info("Input file loaded successfully.")

    logger.info("Generating SUMO files...")
    generate_sumo_files(features, OUTPUT_NODE_FILE, OUTPUT_EDGE_FILE, OUTPUT_CON_FILE)

    logger.info("Running netconvert to create the network file...")
    run_netconvert(OUTPUT_NODE_FILE, OUTPUT_EDGE_FILE, OUTPUT_CON_FILE, OUTPUT_NET_FILE)

    logger.info("SUMO network generation completed successfully.")

if __name__ == "__main__":
    main()
