"""
write_sumo_edges.py

Phase 3: Converts rail_edges_named.csv to SUMO .edg.xml format,
including edge shapes from WKT geometry, with safe edge IDs.

Input:
- data/processed/rail_edges_named.csv

Output:
- sumo/inputs/april_2025_swiss/april_2025_swiss.edg.xml
"""

import pandas as pd
import os
import logging
import re
from shapely import wkt
from shapely.geometry import LineString
from xml.etree.ElementTree import Element, SubElement, ElementTree

# --- Config ---
INPUT_PATH = "data/processed/rail_edges_named.csv"
OUTPUT_PATH = "sumo/inputs/april_2025_swiss/april_2025_swiss.edg.xml"

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def linestring_to_shape(line: LineString) -> str:
    """Converts a Shapely LineString into SUMO shape string: x1,y1 x2,y2 ..."""
    return " ".join([f"{x:.3f},{y:.3f}" for x, y, *_ in line.coords])

def sanitize_edge_id(edge_id: str) -> str:
    """Make edge ID safe for SUMO by replacing/removing invalid characters."""
    edge_id = str(edge_id)
    edge_id = edge_id.replace("&", "and")
    edge_id = re.sub(r"[ ,:()\.\\/\"']", "_", edge_id)
    edge_id = re.sub(r"__+", "_", edge_id)  # Collapse multiple underscores
    return edge_id.strip("_")

def main():
    logging.info("🚀 Generating SUMO .edg.xml from enriched edge file...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    logging.info(f"✅ Loaded {len(df)} edges from: {INPUT_PATH}")
    df["geometry"] = df["geometry"].apply(wkt.loads)

    root = Element("edges")

    for _, row in df.iterrows():
        edge_id = sanitize_edge_id(row["edge_id_human"])
        attrib = {
            "id": edge_id,
            "from": row["from_node"],
            "to": row["to_node"],
        }

        if isinstance(row["geometry"], LineString):
            attrib["shape"] = linestring_to_shape(row["geometry"])

        SubElement(root, "edge", attrib)

    tree = ElementTree(root)
    tree.write(OUTPUT_PATH, encoding="UTF-8", xml_declaration=True)
    logging.info(f"💾 Saved edge file to: {OUTPUT_PATH}")
    logging.info("✅ Phase 3 complete (with sanitized IDs). You may now re-run Phase 5.")

if __name__ == "__main__":
    main()

