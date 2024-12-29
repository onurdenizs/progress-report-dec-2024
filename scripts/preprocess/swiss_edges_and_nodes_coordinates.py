import os
import json
import logging
import utm

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# File paths
geojson_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/raw/swiss/linie_mit_polygon/linie_mit_polygon.geojson"
output_node_file = "D:/PhD/codingPractices/progress-report-dec-2024/sumo/inputs/sw_real_samp/sw_real_comp.nod.xml"
output_edge_file = "D:/PhD/codingPractices/progress-report-dec-2024/sumo/inputs/sw_real_samp/sw_real_comp.edge.xml"
output_con_file = "D:/PhD/codingPractices/progress-report-dec-2024/sumo/inputs/sw_real_samp/sw_real_comp.con.xml"
output_net_file = "D:/PhD/codingPractices/progress-report-dec-2024/sumo/inputs/sw_real_samp/sw_real_comp.net.xml"


def parse_geojson(geojson_path):
    """Parse a GeoJSON file and extract its features.

    Args:
        geojson_path (str): Path to the GeoJSON file.

    Returns:
        list: A list of features extracted from the GeoJSON file.
    """
    with open(geojson_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["features"]


def wgs84_to_utm(lon, lat):
    """Convert WGS84 coordinates to UTM coordinates.

    Args:
        lon (float): Longitude in WGS84.
        lat (float): Latitude in WGS84.

    Returns:
        tuple: UTM x and y coordinates.
    """
    utm_coords = utm.from_latlon(lat, lon)
    return utm_coords[0], utm_coords[1]


def generate_node_id(properties, index):
    """Generate a node ID using station abbreviations.

    Args:
        properties (dict): Properties of the feature.
        index (int): Index of the node in the coordinate list.

    Returns:
        str: Node ID.
    """
    if index == 0:
        return properties.get("bp_anfang", "unknown_start")
    return properties.get("bp_ende", f"unknown_end_{index}")


def create_sumo_files(features, node_file, edge_file, con_file):
    """Create SUMO-compatible node and edge files from GeoJSON features.

    Args:
        features (list): List of features from the GeoJSON file.
        node_file (str): Path to the output node file.
        edge_file (str): Path to the output edge file.
        con_file (str): Path to the output connection file.
    """
    nodes = {}
    edges = {}

    for feature in features:
        geometry = feature["geometry"]
        properties = feature["properties"]
        lininr = properties.get("lininr", "unknown")

        if geometry["type"] == "LineString" and len(geometry["coordinates"]) > 1:
            coordinates = geometry["coordinates"]
            for i, coord in enumerate(coordinates):
                lon, lat = coord
                x, y = wgs84_to_utm(lon, lat)
                node_id = generate_node_id(properties, i)
                if node_id not in nodes:
                    nodes[node_id] = (x, y)

                if i > 0:
                    # Create edge between consecutive nodes
                    prev_node_id = generate_node_id(properties, i - 1)
                    edge_id = f"edge_{prev_node_id}_{node_id}"
                    
                    # Calculate shape for the edge
                    shape_coords = coordinates[i - 1:i + 1]
                    shape = " ".join(
                        f"{wgs84_to_utm(coord[0], coord[1])[0]},{wgs84_to_utm(coord[0], coord[1])[1]}"
                        for coord in shape_coords
                    )
                    
                    # Add edge if not already added
                    if edge_id not in edges:
                        edges[edge_id] = {"from": prev_node_id, "to": node_id, "shape": shape}

    # Write nodes to file
    with open(node_file, "w", encoding="utf-8") as nf:
        nf.write('<nodes>\n')
        for node_id, (x, y) in nodes.items():
            nf.write(f'  <node id="{node_id}" x="{x}" y="{y}" />\n')
        nf.write('</nodes>\n')
    logger.info(f"Node file created: {node_file}")

    # Write edges to file
    with open(edge_file, "w", encoding="utf-8") as ef:
        ef.write('<edges>\n')
        for edge_id, edge_data in edges.items():
            ef.write(
                f'  <edge id="{edge_id}" from="{edge_data["from"]}" to="{edge_data["to"]}" shape="{edge_data["shape"]}" />\n'
            )
        ef.write('</edges>\n')
    logger.info(f"Edge file created: {edge_file}")

    # Write connections file
    with open(con_file, "w", encoding="utf-8") as cf:
        cf.write('<connections>\n</connections>\n')
    logger.info(f"Connection file created: {con_file}")


def run_netconvert(node_file, edge_file, con_file, net_file):
    """Run netconvert to generate the SUMO network.

    Args:
        node_file (str): Path to the node file.
        edge_file (str): Path to the edge file.
        con_file (str): Path to the connection file.
        net_file (str): Path to the output network file.
    """
    command = (
        f'netconvert '
        f'--node-files="{node_file}" '
        f'--edge-files="{edge_file}" '
        f'--connection-files="{con_file}" '
        f'--output-file="{net_file}"'
    )
    logger.info(f"Running netconvert: {command}")
    os.system(command)
    logger.info(f"Network file created: {net_file}")


if __name__ == "__main__":
    logger.info("Starting SUMO network generation...")
    features = parse_geojson(geojson_file)
    create_sumo_files(features, output_node_file, output_edge_file, output_con_file)
    run_netconvert(output_node_file, output_edge_file, output_con_file, output_net_file)
    logger.info("SUMO network generation completed successfully.")
