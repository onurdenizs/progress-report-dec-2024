import geopandas as gpd
from lxml import etree
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# === File paths ===
INPUT_FILE = Path("data/processed/rail_nodes_only.geojson")
OUTPUT_FILE = Path("data/processed/rail_nodes.nod.xml")

logging.info("🚀 Starting Phase 3: Write rail_nodes.nod.xml")

# === Load GeoJSON ===
gdf = gpd.read_file(INPUT_FILE)
logging.info(f"✅ Loaded {len(gdf)} rail nodes")

# === Build XML ===
root = etree.Element("nodes")

for _, row in gdf.iterrows():
    node_id = row["object_id"]
    x, y = row.geometry.x, row.geometry.y  # Already in meters (LV95)
    
    etree.SubElement(root, "node", id=node_id, x=str(x), y=str(y))

# === Write to XML file ===
tree = etree.ElementTree(root)
tree.write(OUTPUT_FILE, pretty_print=True, xml_declaration=True, encoding="UTF-8")

logging.info(f"💾 Wrote node XML to {OUTPUT_FILE.resolve()}")
logging.info("✅ Phase 3 complete")
