"""
Phase 2: Extract Rail Nodes
---------------------------
This script extracts all unique nodes connected to the railway edges,
loads them from the SwissTNE node layer, and saves them to a GeoJSON file.

Output: data/processed/rail_nodes_only.geojson
"""

import geopandas as gpd
import logging
from pathlib import Path
from rich.logging import RichHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[RichHandler(rich_tracebacks=True)]
)

# === File paths ===
DATA_DIR = Path("data")
RAW_FILE = DATA_DIR / "raw" / "swiss" / "swissTNE_Base_20240507.gpkg"
RAIL_EDGES_FILE = DATA_DIR / "processed" / "rail_edges_only.geojson"
OUTPUT_FILE = DATA_DIR / "processed" / "rail_nodes_only.geojson"

# === Start processing ===
logging.info("🚀 Starting Phase 2: Extract Rail Nodes")

# Load rail edges (filtered from Phase 1)
logging.info("📂 Loading rail edges...")
gdf_rail_edges = gpd.read_file(RAIL_EDGES_FILE)

# Extract unique node IDs
from_ids = gdf_rail_edges["from_node_object_id"].dropna().unique()
to_ids = gdf_rail_edges["to_node_object_id"].dropna().unique()
all_node_ids = set(from_ids).union(to_ids)

logging.info(f"🔢 Unique rail node IDs: {len(all_node_ids):,}")

# Load node layer from GeoPackage
logging.info("📂 Reading node layer from SwissTNE GPKG...")
gdf_all_nodes = gpd.read_file(RAW_FILE, layer="bn_node")

# Filter nodes that match IDs used in rail edges
logging.info("🔍 Filtering node layer to only rail nodes...")
gdf_rail_nodes = gdf_all_nodes[gdf_all_nodes["object_id"].isin(all_node_ids)].copy()
logging.info(f"✅ Extracted {len(gdf_rail_nodes):,} rail nodes")

# Save result
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
gdf_rail_nodes.to_file(OUTPUT_FILE, driver="GeoJSON")
logging.info(f"💾 Saved rail nodes to {OUTPUT_FILE}")
logging.info("✅ Phase 2 complete")

