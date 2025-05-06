"""
assign_human_friendly_names.py

Phase 1B: Matches each rail node to the nearest official station name
using haltestelle-haltekante.csv via spatial join.

Input:
- data/processed/rail_nodes.csv
- data/raw/swiss/haltestelle-haltekante.csv

Output:
- data/processed/rail_nodes_named.csv
"""

import pandas as pd
import geopandas as gpd
import logging
from shapely.geometry import Point
import os

# --- Config ---
RAIL_NODE_PATH = "data/processed/rail_nodes.csv"
STOP_CSV_PATH = "data/raw/swiss/haltestelle-haltekante.csv"
OUTPUT_PATH = "data/processed/rail_nodes_named.csv"
CRS = 2056
JOIN_TOLERANCE_METERS = 100

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def parse_lat_lon_string(val):
    """Parses 'lat, lon' string into (x, y) = (lon, lat) tuple."""
    try:
        lat_str, lon_str = val.strip().split(",")
        return float(lon_str), float(lat_str)
    except Exception:
        return None, None

def main():
    logging.info("🚀 Script started. Beginning node-stop matching process...")
    os.makedirs("data/processed", exist_ok=True)

    # --- Load Rail Nodes ---
    logging.info("📥 Loading rail node data...")
    nodes_df = pd.read_csv(RAIL_NODE_PATH)
    logging.info(f"✅ Loaded {len(nodes_df)} nodes.")
    nodes_gdf = gpd.GeoDataFrame(
        nodes_df,
        geometry=gpd.points_from_xy(nodes_df["x"], nodes_df["y"]),
        crs=f"EPSG:{CRS}"
    )

    # --- Load Stops ---
    logging.info("📥 Loading stop data...")
    stops_df = pd.read_csv(STOP_CSV_PATH, sep=";", dtype=str)
    stops_df["lon"], stops_df["lat"] = zip(*stops_df["geopos_haltestelle"].apply(parse_lat_lon_string))
    stops_df = stops_df.dropna(subset=["lat", "lon"])
    logging.info(f"✅ Valid stops with coordinates: {len(stops_df)}")

    stops_gdf = gpd.GeoDataFrame(
        stops_df,
        geometry=gpd.points_from_xy(stops_df["lon"], stops_df["lat"]),
        crs="EPSG:4326"
    ).to_crs(epsg=CRS)

    # --- Spatial Join ---
    logging.info(f"🔗 Performing nearest spatial join (tolerance {JOIN_TOLERANCE_METERS}m)...")
    matched_gdf = gpd.sjoin_nearest(
        nodes_gdf,
        stops_gdf[["offizielle Haltestellen Bezeichnung", "geometry"]],
        how="left",
        max_distance=JOIN_TOLERANCE_METERS,
        distance_col="distance"
    )

    # Rename the station name column for clarity
    matched_gdf = matched_gdf.rename(columns={"offizielle Haltestellen Bezeichnung": "station_name"})

    # Clean and export
    matched_gdf.drop(columns=["geometry", "index_right", "distance"], errors="ignore").to_csv(OUTPUT_PATH, index=False)
    logging.info(f"💾 Saved enriched node data: {OUTPUT_PATH}")
    logging.info("✅ Done. Proceed to human-friendly edge naming.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("🔥 Script crashed!", exc_info=True)
