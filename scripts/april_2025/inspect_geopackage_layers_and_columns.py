"""
inspect_geopackage_layers_and_columns.py

Inspects the SwissTNE GeoPackage file to list available layers and their columns.
Use this script to identify correct layer names and available columns
before filtering for specific features like railway nodes and edges.

Author: Onur Deniz
"""

import geopandas as gpd
import fiona
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# GeoPackage path (update if needed)
GPKG_PATH = Path("data/raw/swiss/swissTNE_Base_20240507.gpkg")

def inspect_geopackage(gpkg_path: Path):
    """List layers and their columns in the specified GeoPackage."""
    logging.info(f"🔍 Inspecting GeoPackage: {gpkg_path}")
    
    layers = fiona.listlayers(gpkg_path)
    logging.info(f"📚 Found {len(layers)} layers: {layers}")

    for layer in layers:
        logging.info(f"📂 Reading layer: {layer}")
        gdf = gpd.read_file(gpkg_path, layer=layer)
        logging.info(f"✅ Layer '{layer}' contains {len(gdf)} rows and {len(gdf.columns)} columns.")
        logging.info(f"📌 Columns: {list(gdf.columns)}\n")

if __name__ == "__main__":
    inspect_geopackage(GPKG_PATH)
