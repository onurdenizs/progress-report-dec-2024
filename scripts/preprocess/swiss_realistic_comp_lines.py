import os
import json
import logging
from pyproj import Transformer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# File paths
GEOJSON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\normalized_swiss_lines.geojson"
OUTPUT_NODE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.nod.xml"
OUTPUT_EDGE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.edge.xml"
OUTPUT_CON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.con.xml"
OUTPUT_NET_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.net.xml"

# Parameters
V_MAX_KMH = 250  # Maximum speed in km/h
V_MAX_MS = round(V_MAX_KMH / 3.6, 2)  # Convert to m/s
BIDIRECTIONAL = True

# Initialize Transformer for WGS84 to UTM32
transformer = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)

def wgs84_to_utm(lon, lat, precision=3):
    """Convert WGS84 coordinates to UTM and round them to a given precision."""
    utm_x, utm_y = transformer.transform(lon, lat)
    return round(utm_x, precision), round(utm_y, precision)

def load_geojson(file_path):
    """Load GeoJSON file and return its content.
    Args:
        file_path (str): Path to the GeoJSON file.
    Returns:
        dict: Parsed GeoJSON content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load GeoJSON file: {e}")
        raise

def generate_sumo_files(features, node_file, edge_file, con_file):
    """Generate SUMO node, edge, and connection files from GeoJSON data.
    Args:
        features (list): List of GeoJSON features.
        node_file (str): Path to the node XML file.
        edge_file (str): Path to the edge XML file.
        con_file (str): Path to the connection XML file.
    """
    nodes = {}
    edges = []

    def add_node(node_id, lon, lat):
        """Add a node if it does not already exist.
        Args:
            node_id (str): Node ID.
            lon (float): Longitude.
            lat (float): Latitude.
        Returns:
            tuple: Node ID and its UTM coordinates.
        """
        utm_x, utm_y = wgs84_to_utm(lon, lat)
        if node_id not in nodes:
            nodes[node_id] = (utm_x, utm_y)
        return node_id, utm_x, utm_y

    for feature in features:
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        linienr = properties.get("linienr", "unknown")
        bp_anfang = properties.get("bp_anfang", "unknown_start")
        bp_ende = properties.get("bp_ende", "unknown_end")

        if geometry.get("type") == "LineString" and len(geometry.get("coordinates", [])) > 1:
            coords = geometry["coordinates"]
            
            # Add start node
            start_lon, start_lat = coords[0]
            start_node_id, _, _ = add_node(bp_anfang, start_lon, start_lat)
            
            # Add end node
            end_lon, end_lat = coords[-1]
            end_node_id, _, _ = add_node(bp_ende, end_lon, end_lat)
            
            prev_node_id = start_node_id
            for i, (lon, lat) in enumerate(coords[1:], start=1):
                current_node_id, utm_x, utm_y = add_node(f"{start_node_id}_{end_node_id}_{i}", lon, lat)
                
                # Skip zero-length edges
                if prev_node_id != current_node_id:
                    edges.append({
                        "id": f"edge_{prev_node_id}_{current_node_id}",
                        "from": prev_node_id,
                        "to": current_node_id,
                        "shape": f"{nodes[prev_node_id][0]},{nodes[prev_node_id][1]} {utm_x},{utm_y}",
                        "v_max": V_MAX_MS
                    })
                    prev_node_id = current_node_id

            # Connect last intermediate node to the end node
            if prev_node_id != end_node_id:
                edges.append({
                    "id": f"edge_{prev_node_id}_{end_node_id}",
                    "from": prev_node_id,
                    "to": end_node_id,
                    "shape": f"{nodes[prev_node_id][0]},{nodes[prev_node_id][1]} {nodes[end_node_id][0]},{nodes[end_node_id][1]}",
                    "v_max": V_MAX_MS
                })

    # Write Node file
    with open(node_file, "w", encoding="utf-8") as nf:
        nf.write("<nodes>\n")
        for node_id, (x, y) in nodes.items():
            nf.write(f'  <node id="{node_id}" x="{x}" y="{y}" />\n')
        nf.write("</nodes>\n")
    logger.info(f"Node file created: {node_file}")

    # Write Edge file
    with open(edge_file, "w", encoding="utf-8") as ef:
        ef.write("<edges>\n")
        for edge in edges:
            ef.write(
                f'  <edge id="{edge["id"]}" from="{edge["from"]}" to="{edge["to"]}" '
                f'priority="1" numLanes="1" speed="{edge["v_max"]}" shape="{edge["shape"]}" />\n'
            )
        ef.write("</edges>\n")
    logger.info(f"Edge file created: {edge_file}")

    # Write Connection file (empty for now)
    with open(con_file, "w", encoding="utf-8") as cf:
        cf.write("<connections>\n</connections>\n")
    logger.info(f"Connection file created: {con_file}")

def run_netconvert(node_file, edge_file, con_file, net_file):
    """Run netconvert to generate the SUMO network file.
    Args:
        node_file (str): Path to node XML file.
        edge_file (str): Path to edge XML file.
        con_file (str): Path to connection XML file.
        net_file (str): Path to output SUMO network file.
    """
    command = (
        f'netconvert --node-files="{node_file}" '
        f'--edge-files="{edge_file}" '
        f'--connection-files="{con_file}" '
        f'--output-file="{net_file}" --precision=6 --remove-edges.by-vclass rail'
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
