"""
validate_all_route_edges_against_net.py

Checks all mapped route XML files in `mapped_rou/` folder to ensure
each edge in the route is present in the compiled SUMO network (.net.xml).

Author: GPT-4 + Onur | April 2025
"""

import os
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Paths
NET_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\april_2025_swiss\april_2025_swiss.net.xml"
ROUTE_FOLDER = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\mapped_rou"

def get_valid_edge_ids(net_file):
    logging.info(f"📥 Loading edge IDs from network: {net_file}")
    tree = ET.parse(net_file)
    root = tree.getroot()
    return set(edge.attrib["id"] for edge in root.findall(".//edge") if "id" in edge.attrib)

def validate_route(route_file, valid_edges):
    invalid_entries = []
    tree = ET.parse(route_file)
    for vehicle in tree.findall(".//vehicle"):
        veh_id = vehicle.attrib.get("id", "unknown")
        for route in vehicle.findall(".//route"):
            if "edges" in route.attrib:
                edge_ids = route.attrib["edges"].split()
                for eid in edge_ids:
                    if eid not in valid_edges:
                        invalid_entries.append((veh_id, eid))
    return invalid_entries

def main():
    valid_edges = get_valid_edge_ids(NET_PATH)
    logging.info(f"✅ Loaded {len(valid_edges):,} valid edges from network.")
    
    all_issues = []
    route_files = [f for f in os.listdir(ROUTE_FOLDER) if f.endswith(".rou.xml")]

    logging.info(f"🔎 Validating {len(route_files)} route files in: {ROUTE_FOLDER}")
    
    for rf in route_files:
        route_path = os.path.join(ROUTE_FOLDER, rf)
        issues = validate_route(route_path, valid_edges)
        if issues:
            logging.warning(f"❌ Found {len(issues)} invalid edge(s) in {rf}:")
            for veh_id, eid in issues:
                logging.warning(f" → Vehicle '{veh_id}' references unknown edge '{eid}'")
            all_issues.extend([(rf, veh_id, eid) for veh_id, eid in issues])
        else:
            logging.info(f"✅ {rf} is valid.")

    if all_issues:
        logging.info(f"🚨 Summary: {len(all_issues)} invalid edge references found across {len(route_files)} file(s).")
    else:
        logging.info("🎉 All route files are clean and match the network.")

if __name__ == "__main__":
    main()
