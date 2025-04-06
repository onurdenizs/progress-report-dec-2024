import geopandas as gpd
import pandas as pd
from lxml import etree
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# === File paths ===
EDGES_FILE = Path("data/processed/rail_edges_only.geojson")
NODES_FILE = Path("data/processed/rail_nodes_only.geojson")
OUTPUT_FILE = Path("data/processed/rail_edges.edg.xml")

logging.info("🚀 Starting Phase 4 (Fixed): Write rail_edges.edg.xml")

# === Load data ===
gdf_edges = gpd.read_file(EDGES_FILE)
logging.info(f"✅ Loaded {len(gdf_edges)} rail edges")

gdf_nodes = gpd.read_file(NODES_FILE)
valid_node_ids = set(gdf_nodes["object_id"])
logging.info(f"✅ Loaded {len(valid_node_ids)} rail nodes")

# === Prepare XML ===
root = etree.Element("edges")
skipped = 0
used_ids = set()

for _, row in gdf_edges.iterrows():
    from_node = row["from_node_object_id"]
    to_node = row["to_node_object_id"]

    # Skip if from/to node not in node list
    if from_node not in valid_node_ids or to_node not in valid_node_ids:
        skipped += 1
        continue

    # Build readable edge ID
    edge_id = f"edge_{from_node}_{to_node}"
    if edge_id in used_ids:
        logging.warning(f"⚠️ Duplicate edge ID detected: {edge_id}")
        continue
    used_ids.add(edge_id)

    # Build shape string
    shape = " ".join(f"{pt[0]},{pt[1]}" for pt in row.geometry.coords)

    # Use a dict to avoid Python's reserved keyword 'from'
    etree.SubElement(root, "edge", attrib={
        "id": edge_id,
        "from": from_node,
        "to": to_node,
        "shape": shape
    })

# === Write to XML ===
tree = etree.ElementTree(root)
tree.write(OUTPUT_FILE, pretty_print=True, xml_declaration=True, encoding="UTF-8")

logging.info(f"💾 Wrote edge XML to {OUTPUT_FILE.resolve()}")
logging.info(f"✅ Phase 4 complete — Skipped {skipped} edges with missing nodes")
