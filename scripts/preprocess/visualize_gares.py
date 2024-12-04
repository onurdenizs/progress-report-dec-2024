"""
visualize_gares.py

Script to read and visualize French train stations from gares.geojson.
Creates an interactive zoomable map of station locations, saves the visualization as an HTML file, 
and exports a high-resolution PNG image.
"""

import geopandas as gpd
import plotly.express as px
import os

# File paths
input_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/raw/french/gares/gares.geojson"
output_dir = "D:/PhD/codingPractices/progress-report-dec-2024/outputs/visualizations/french"
output_html = os.path.join(output_dir, "gares_map.html")
output_png = os.path.join(output_dir, "gares_map.png")

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

    print("Creating the visualization...")
    # Extract coordinates for Plotly visualization
    gdf["longitude"] = gdf.geometry.x
    gdf["latitude"] = gdf.geometry.y

    # Create an interactive map
    fig = px.scatter_mapbox(
        gdf,
        lat="latitude",
        lon="longitude",
        hover_name="nom",  # Corrected column name for station name
        hover_data=["libellecourt", "codes_uic"],  # Adjust as needed
        zoom=6,  # Adjust initial zoom level
        mapbox_style="open-street-map",
        title="French Train Stations (Zoomable Map)"
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
except Exception as e:
    print(f"An unexpected error occurred: {e}")
