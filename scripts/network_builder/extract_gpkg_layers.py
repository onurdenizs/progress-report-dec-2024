"""
Phase 1: Load and filter rail edges from SwissTNE Base GPKG.
Goal: Extract only the edges that represent rail infrastructure.
"""

import geopandas as gpd
from pathlib import Path
from loguru import logger

# === Config ===
data_file = Path("D:/PhD/codingPractices/progress-report-dec-2024/data/raw/swiss/swissTNE_Base_20240507.gpkg")
layer_edges = "bn_edge"
layer_nodes = "bn_node"
layer_basetype = "lut_base_type"

# === Logging ===
logger.add("phase1_extract_rail_edges.log", rotation="500 KB")
logger.info("Starting Phase 1: Extract rail edges")

# === Load edge and basetype layers ===
logger.info("Reading edge layer...")
gdf_edges = gpd.read_file(data_file, layer=layer_edges)
logger.info(f"✅ Loaded {len(gdf_edges)} edges")

logger.info("Reading basetype lookup table...")
df_basetype = gpd.read_file(data_file, layer=layer_basetype)

# === Check types and convert for merging ===
gdf_edges["basetype"] = gdf_edges["basetype"].astype(str)
df_basetype["object_key"] = df_basetype["object_key"].astype(str)

# === Merge basetype labels into edges ===
gdf_edges = gdf_edges.merge(df_basetype[["object_key", "value_short_en"]],
                            how="left", left_on="basetype", right_on="object_key")
gdf_edges.rename(columns={"value_short_en": "basetype_label"}, inplace=True)
logger.info("✅ Merged basetype labels")

# === Filter for rail-only edges ===
gdf_rail = gdf_edges[gdf_edges["basetype_label"] == "ra"].copy()
logger.info(f"🚆 Extracted {len(gdf_rail)} rail edges")

# === Save filtered rail edges (optional for debugging) ===
out_path = Path("data/processed/rail_edges_only.geojson")
out_path.parent.mkdir(parents=True, exist_ok=True)
gdf_rail.to_file(out_path, driver="GeoJSON")
logger.success(f"Saved rail edges to {out_path}")

logger.success("✅ Phase 1 complete")
