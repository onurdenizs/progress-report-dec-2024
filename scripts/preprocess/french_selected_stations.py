"""
french_selected_stations.py

Script to filter and visualize five selected French train stations on an interactive map.
Saves the visualization as both an HTML file and a high-resolution PNG image.
"""

import geopandas as gpd
import plotly.express as px
import os

# File paths
input_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/raw/french/gares/gares.geojson"
output_dir = "D:/PhD/codingPractices/progress-report-dec-2024/outputs/visualizations/french"
output_html = os.path.join(output_dir, "selected_gares_map.html")
output_png = os.path.join(output_dir, "selected_gares_map.png")

# List of station names to focus on
selected_stations = [
    "Paris Gare de Lyon",  # Paris (PLY)
    "Strasbourg",          # Strasbourg (STG)
    "Nantes",              # Nantes (NTS)
    "Rennes",              # Rennes (RES)
    "Dijon"                # Dijon (DJV)
]

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

try:
    print("Loading the gares.geojson dataset...")
    # Load the dataset
    gdf = gpd.read_file(input_file)
    print("Dataset loaded successfully!")

    # Check for geometry column
    if "geometry" not in gdf.columns:
        raise ValueError("No geometry column found in the dataset.")

    print(f"Filtering for selected stations: {selected_stations}...")
    # Filter the dataset for the selected stations
    filtered_gdf = gdf[gdf["nom"].isin(selected_stations)]

    if filtered_gdf.empty:
        raise ValueError("No stations found matching the specified names.")

    print("Creating the visualization...")
    # Extract coordinates for Plotly visualization
    filtered_gdf["longitude"] = filtered_gdf.geometry.x
    filtered_gdf["latitude"] = filtered_gdf.geometry.y

    # Create an interactive map
    fig = px.scatter_mapbox(
        filtered_gdf,
        lat="latitude",
        lon="longitude",
        hover_name="nom",  # Station name
        hover_data=["libellecourt", "codes_uic"],  # Additional details
        zoom=5,  # Adjust initial zoom level
        mapbox_style="open-street-map",
        title="Selected French Train Stations (Zoomable Map)"
    )

    print(f"Saving the visualization to {output_html}...")
    # Save the visualization as an HTML file
    fig.write_html(output_html)

    print(f"Saving the high-resolution image to {output_png}...")
    # Save the visualization as a high-resolution PNG file
    fig.write_image(output_png, width=1920, height=1080, scale=3)
    print("Visualization saved successfully!")

except FileNotFoundError:
    print(f"Error: The file {input_file} was not found.")
except ValueError as ve:
    print(f"Error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
