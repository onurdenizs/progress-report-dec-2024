"""
extract_nodes_and_edges.py

Phase 1 of April 2025 SUMO Swiss Network Pipeline.
Extracts raw rail node and edge data from SwissTNE GeoPackage,
projects to EPSG:2056, and saves to CSV for further enrichment.

Author: Onur Deniz
Date: 2025-04
"""

import geopandas as gpd
import pandas as pd
import logging
import os

# --- Configuration ---
INPUT_GPKG = "data/raw/swiss/swissTNE_Base_20240507.gpkg"
OUTPUT_DIR = "data/processed/"
NODE_LAYER = "bn_node"
EDGE_LAYER = "bn_edge"
CRS_TARGET = 2056  # EPSG:2056 (LV95 / CH1903+)

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def load_and_project_layer(gpkg_path, layer_name, target_crs):
    """Loads and projects a GeoPackage layer."""
    logging.info(f"📂 Reading layer '{layer_name}' from {gpkg_path}")
    gdf = gpd.read_file(gpkg_path, layer=layer_name)
    logging.info(f"✅ Loaded {len(gdf)} rows from '{layer_name}'")
    return gdf.to_crs(epsg=target_crs)

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # --- Nodes ---
    gdf_nodes = load_and_project_layer(INPUT_GPKG, NODE_LAYER, CRS_TARGET)
    gdf_nodes["node_id"] = "n_" + gdf_nodes["object_id"].astype(str)
    gdf_nodes["x"] = gdf_nodes.geometry.x
    gdf_nodes["y"] = gdf_nodes.geometry.y

    node_cols = ["node_id", "object_id", "x", "y", "geometry"]
    node_path = os.path.join(OUTPUT_DIR, "rail_nodes.csv")
    gdf_nodes[node_cols].to_csv(node_path, index=False)
    logging.info(f"💾 Saved: {node_path} ({len(gdf_nodes)} rows)")

    # --- Edges ---
    gdf_edges = load_and_project_layer(INPUT_GPKG, EDGE_LAYER, CRS_TARGET)
    gdf_edges["edge_id"] = "e_" + gdf_edges["object_id"].astype(str)
    gdf_edges["from_node"] = "n_" + gdf_edges["from_node_object_id"].astype(str)
    gdf_edges["to_node"] = "n_" + gdf_edges["to_node_object_id"].astype(str)
    gdf_edges["length"] = gdf_edges["m_length"]

    edge_cols = ["edge_id", "object_id", "from_node", "to_node", "length", "geometry"]
    edge_path = os.path.join(OUTPUT_DIR, "rail_edges.csv")
    gdf_edges[edge_cols].to_csv(edge_path, index=False)
    logging.info(f"💾 Saved: {edge_path} ({len(gdf_edges)} rows)")

    logging.info("✅ Phase 1 complete. Proceed to assign_human_friendly_names.py")

if __name__ == "__main__":
    main()
