"""
match_gtfs_stops_to_sumo_edges.py

Fix: Uses 'edge_id_human' instead of 'edge_id' to write valid SUMO-compatible routes.

Author: GPT-4 + Onur | April 2025
"""

import os
import glob
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import logging

# ----------------------------------------
# Config paths
# ----------------------------------------

STOP_FOLDER = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\stop_sequences"
STOPS_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\gtfs_ftp_2025\stops.txt"
EDGE_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\rail_edges_named.csv"
OUTPUT_FOLDER = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\mapped_rou"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

PROJECTION = "EPSG:2056"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def load_edges(edge_path):
    df = pd.read_csv(edge_path)
    df = df.dropna(subset=["geometry"])
    df["geometry"] = gpd.GeoSeries.from_wkt(df["geometry"])
    return gpd.GeoDataFrame(df, geometry="geometry", crs=PROJECTION)


def find_closest_edge(point, edge_gdf):
    distances = edge_gdf.distance(point)
    idx = distances.idxmin()
    return edge_gdf.loc[idx, "edge_id_human"]


def build_route_file(route_id, edge_ids, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("<routes>\n")
        f.write(f'    <vehicle id="{route_id}" type="IC" depart="0">\n')
        f.write(f'        <route edges="{" ".join(edge_ids)}"/>\n')
        f.write("    </vehicle>\n")
        f.write("</routes>\n")


def main():
    logging.info("📍 Loading SUMO rail edge geometries...")
    edge_gdf = load_edges(EDGE_FILE)

    logging.info("📥 Loading GTFS stop coordinates from stops.txt...")
    stops_df = pd.read_csv(STOPS_FILE, dtype={"stop_id": str})
    stops_df = stops_df.dropna(subset=["stop_lat", "stop_lon"])
    stops_df = stops_df[["stop_id", "stop_lat", "stop_lon"]].copy()
    stops_df["stop_id"] = stops_df["stop_id"].astype(str)

    stop_files = glob.glob(os.path.join(STOP_FOLDER, "*.csv"))

    for stop_file in stop_files:
        route_id = os.path.basename(stop_file).replace("_stops.csv", "")
        logging.info(f"🔁 Processing route: {route_id}")

        df = pd.read_csv(stop_file, dtype={"stop_id": str})
        if "stop_id" not in df.columns:
            logging.warning(f"⚠️ Skipping {route_id} — no 'stop_id' found.")
            continue

        merged = pd.merge(df, stops_df, on="stop_id", how="left")
        if merged["stop_lat"].isna().any():
            logging.warning(f"⚠️ Skipping {route_id} — missing stop coordinates after merge.")
            continue

        gdf = gpd.GeoDataFrame(
            merged,
            geometry=[Point(lon, lat) for lon, lat in zip(merged["stop_lon"], merged["stop_lat"])],
            crs="EPSG:4326"
        ).to_crs(PROJECTION)

        edge_ids = []
        for pt in gdf.geometry:
            edge_id = find_closest_edge(pt, edge_gdf)
            edge_ids.append(edge_id)

        output_path = os.path.join(OUTPUT_FOLDER, f"mapped_routes_{route_id}.rou.xml")
        build_route_file(route_id, edge_ids, output_path)
        logging.info(f"✅ Saved: {output_path}")


if __name__ == "__main__":
    main()
