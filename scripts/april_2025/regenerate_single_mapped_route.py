"""
regenerate_single_mapped_route.py

Regenerates a single mapped SUMO route file using GTFS stop coordinates
and nearest edge matching in the rail network.

Author: GPT-4 + Onur | April 2025
"""

import os
import pandas as pd
import geopandas as gpd
import logging
from shapely.geometry import Point
from shapely.ops import nearest_points

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Inputs
TARGET_ROUTE_ID = "91-29-Y-j25-1"
STOPS_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\gtfs_ftp_2025\stops.txt"
STOP_SEQUENCE_PATH = fr"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\stop_sequences\{TARGET_ROUTE_ID}_stops.csv"
EDGE_PATH = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\rail_edges_named.csv"
OUTPUT_ROU_PATH = fr"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\routes\mapped_rou\mapped_routes_{TARGET_ROUTE_ID}.rou.xml"

def main():
    logging.info(f"🔁 Regenerating route for: {TARGET_ROUTE_ID}")

    # Load GTFS stops
    stops_df = pd.read_csv(STOPS_PATH)
    stops_df = stops_df.rename(columns={"stop_id": "stop_id", "stop_lat": "lat", "stop_lon": "lon"})
    stops_df = stops_df.dropna(subset=["lat", "lon"])

    # Load stop sequence for target route
    route_stops = pd.read_csv(STOP_SEQUENCE_PATH)
    route_stops = route_stops.merge(stops_df, on="stop_id", how="left")
    route_stops = route_stops.dropna(subset=["lat", "lon"])
    stop_gdf = gpd.GeoDataFrame(route_stops, geometry=gpd.points_from_xy(route_stops["lon"], route_stops["lat"]), crs="EPSG:4326").to_crs(epsg=2056)

    # Load rail edges
    edge_df = pd.read_csv(EDGE_PATH)
    edge_df = edge_df.dropna(subset=["geometry"])
    edge_gdf = gpd.GeoDataFrame(edge_df, geometry=edge_df["geometry"].apply(wkt.loads), crs="EPSG:2056")

    # Find nearest edge to each stop
    matched_edges = []
    for stop in stop_gdf.itertuples():
        nearest = edge_gdf.distance(stop.geometry).sort_values().index[0]
        edge_id = edge_gdf.loc[nearest, "edge_id"]
        matched_edges.append(edge_id)

    # Generate route XML
    with open(OUTPUT_ROU_PATH, "w", encoding="utf-8") as f:
        f.write("<routes>\n")
        f.write('    <vehicle id="{0}" type="IC" depart="0">\n'.format(TARGET_ROUTE_ID))
        f.write('        <route edges="{0}"/>\n'.format(" ".join(matched_edges)))
        f.write("    </vehicle>\n")
        f.write("</routes>\n")

    logging.info(f"✅ Saved regenerated file: {OUTPUT_ROU_PATH}")

if __name__ == "__main__":
    from shapely import wkt
    main()
