"""
visualize_readable_edges_map.py

Visualizes readable railway edges on an interactive Leaflet map using Folium.

Input:
- data/processed/rail_edges_named.csv

Output:
- outputs/interactive_readable_edges_map.html

Usage:
Run this script locally. Opens map in browser after creation.

Author: Onur Deniz
Date: 2025-04
"""

import os
import pandas as pd
import geopandas as gpd
from shapely import wkt
import folium
import webbrowser

# --- Config ---
INPUT_PATH = "data/processed/rail_edges_named.csv"
OUTPUT_DIR = "outputs"
OUTPUT_HTML = os.path.join(OUTPUT_DIR, "interactive_readable_edges_map.html")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("📥 Reading edge data...")
    df = pd.read_csv(INPUT_PATH)

    print("🔍 Filtering readable edges...")
    df = df[(~df["from_station"].isna()) & (~df["to_station"].isna())].copy()

    print(f"✅ {len(df)} readable edges found.")

    # Convert WKT to geometry
    df["geometry"] = df["geometry"].apply(wkt.loads)
    gdf = gpd.GeoDataFrame(df, geometry="geometry", crs="EPSG:2056")
    gdf = gdf.to_crs(epsg=4326)  # WGS84 for folium

    print("🗺️ Creating map...")
    m = folium.Map(location=[46.8, 8.3], zoom_start=8, tiles="CartoDB positron")

    for _, row in gdf.iterrows():
        folium.PolyLine(
            locations=[(pt[1], pt[0]) for pt in row.geometry.coords],
            tooltip=row["edge_id_human"],
            color="blue",
            weight=2,
            opacity=0.6
        ).add_to(m)

    m.save(OUTPUT_HTML)
    print(f"💾 Map saved to: {OUTPUT_HTML}")
    webbrowser.open(OUTPUT_HTML)

if __name__ == "__main__":
    main()
