import json
import logging
from pyproj import Transformer

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# File paths
INPUT_GEOJSON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon_altered.geojson"
OUTPUT_NODE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.nod.xml"
OUTPUT_EDGE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.edge.xml"
OUTPUT_CON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.con.xml"
OUTPUT_NET_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_comp.net.xml"

# Detection thresholds
SHARP_TURN_THRESHOLD = 10.0  # Meters
SHORT_CONNECTION_THRESHOLD = 1.0  # Meters
# Parameters
V_MAX_KMH = 250  # Maximum speed in km/h
V_MAX_MS = round(V_MAX_KMH / 3.6, 2)  # Convert to m/s
BIDIRECTIONAL = True
# Initialize Transformer
transformer = Transformer.from_crs("epsg:4326", "epsg:32632", always_xy=True)

def wgs84_to_utm(lon, lat):
    """Convert WGS84 to UTM."""
    return transformer.transform(lon, lat)

def calculate_distance(coord1, coord2):
    """Calculate Euclidean distance."""
    return ((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2) ** 0.5

def detect_and_adjust_segments(features):
    """Detect and summarize problematic segments."""
    adjustment_summary = {}

    for feature in features:
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        coordinates = geometry.get("coordinates", [])
        segment_id = f"{properties.get('bp_anfang')} -> {properties.get('bp_ende')}"

        if geometry.get("type") == "LineString" and len(coordinates) >= 2:
            utm_coords = [wgs84_to_utm(lon, lat) for lon, lat in coordinates]

            for i in range(len(utm_coords) - 1):
                dist = calculate_distance(utm_coords[i], utm_coords[i + 1])
                if dist < SHORT_CONNECTION_THRESHOLD:
                    adjustment_summary.setdefault(segment_id, []).append(
                        {"type": "Short Connection", "index": i, "distance": dist}
                    )

            for i in range(1, len(utm_coords) - 1):
                prev, current, next_ = utm_coords[i - 1], utm_coords[i], utm_coords[i + 1]
                radius = calculate_distance(prev, next_) / 2
                if radius < SHARP_TURN_THRESHOLD:
                    adjustment_summary.setdefault(segment_id, []).append(
                        {"type": "Sharp Turn", "index": i, "radius": radius}
                    )

    # Log the summary
    for segment, issues in adjustment_summary.items():
        logger.info(f"Segment {segment} has {len(issues)} adjustments:")
        for issue in issues:
            logger.info(f"  {issue['type']} at index {issue['index']}, value: {issue.get('distance', issue.get('radius'))}")

    return features

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

    edge_connections = {}

    for feature in features:
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        bp_anfang = properties.get("bp_anfang", "unknown_start")
        bp_ende = properties.get("bp_ende", "unknown_end")
        

        if geometry.get("type") == "LineString" and len(geometry.get("coordinates", [])) > 1:
            # Extract WGS84 geolist
            wgs84_geolist = geometry["coordinates"][:]
            

            # Convert WGS84 to UTM
            utm_geolist = [wgs84_to_utm(lon, lat) for lon, lat in wgs84_geolist]
            

            # Create start node (SURB)
            start_coord = utm_geolist.pop(0)
            

            start_node_id, start_utm_x, start_utm_y = add_node(bp_anfang, *start_coord)
            
            # Create end node (ZIE)
            end_coord = utm_geolist.pop(-1)
            

            end_node_id, end_utm_x, end_utm_y = add_node(bp_ende, *end_coord)
            
            prev_node_id = start_node_id

            # Process intermediate nodes
            for i, (utm_x, utm_y) in enumerate(utm_geolist, start=1):
                current_node_id, _, _ = add_node(f"{bp_anfang}_{bp_ende}_{i:04d}", utm_x, utm_y)
                edge_id = f"edge_{prev_node_id}_{current_node_id}"
                edges.append({
                    "id": edge_id,
                    "from": prev_node_id,
                    "to": current_node_id,
                    "shape": f"{nodes[prev_node_id][0]},{nodes[prev_node_id][1]} {utm_x},{utm_y}",
                    "v_max": V_MAX_MS,
                    "type": "railway"
                })
                prev_node_id = current_node_id

            # Add final connection to the end node
            edge_id = f"edge_{prev_node_id}_{end_node_id}"
            edges.append({
                "id": edge_id,
                "from": prev_node_id,
                "to": end_node_id,
                "shape": f"{nodes[prev_node_id][0]},{nodes[prev_node_id][1]} {nodes[end_node_id][0]},{nodes[end_node_id][1]}",
                "v_max": V_MAX_MS,
                "type": "railway"
            })

    # Generate junction connections
    for node_id, edge_list in edge_connections.items():
        incoming_edges = [edge for edge in edges if edge['to'] == node_id]
        outgoing_edges = [edge for edge in edges if edge['from'] == node_id]

        for incoming_edge in incoming_edges:
            for outgoing_edge in outgoing_edges:
                connections.append({
                    "from": incoming_edge['id'],
                    "to": outgoing_edge['id'],
                    "fromLane": "0",
                    "toLane": "0"
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

    # Write Connection file
    with open(con_file, "w", encoding="utf-8") as cf:
        cf.write("<connections>\n")
        for conn in connections:
            cf.write(f'  <connection from="{conn["from"]}" to="{conn["to"]}" fromLane="{conn["fromLane"]}" toLane="{conn["toLane"]}" />\n')
        cf.write("</connections>\n")
    logger.info(f"Connection file created: {con_file}")

def run_netconvert(node_file, edge_file, con_file, net_file):
    """Placeholder for netconvert execution."""
    logger.info(f"Running netconvert for network generation.")

def main():
    """Main function."""
    logger.info("Loading input GeoJSON file...")
    with open(INPUT_GEOJSON_FILE, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
    logger.info("Input file loaded successfully.")

    features = geojson_data.get("features", [])
    logger.info("Detecting and summarizing problematic segments...")
    adjusted_features = detect_and_adjust_segments(features)

    # Generate SUMO files
    generate_sumo_files(adjusted_features, OUTPUT_NODE_FILE, OUTPUT_EDGE_FILE, OUTPUT_CON_FILE)

    # Run netconvert
    run_netconvert(OUTPUT_NODE_FILE, OUTPUT_EDGE_FILE, OUTPUT_CON_FILE, OUTPUT_NET_FILE)

    logger.info("Process completed successfully.")

if __name__ == "__main__":
    main()
