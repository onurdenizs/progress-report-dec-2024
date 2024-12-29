import geopandas as gpd
from shapely.geometry import LineString, MultiLineString
from collections import defaultdict
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Input and output file paths
input_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon.geojson"
output_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\normalized_swiss_lines.geojson"

def normalize_geometry():
    """Normalize station coordinates and geometries for SUMO network generation."""
    try:
        # Step 1: Load the input file
        logger.info("Loading input GeoJSON file...")
        linie_df = gpd.read_file(input_file)

        # Step 2: Build a reference coordinate dictionary
        logger.info("Building reference coordinates for each station...")
        station_coordinates = defaultdict(list)

        for _, row in linie_df.iterrows():
            bp_anfang, bp_ende = row["bp_anfang"], row["bp_ende"]
            coordinates = list(row["geometry"].coords)

            # Collect coordinates for both stations
            station_coordinates[bp_anfang].append(coordinates[0])
            station_coordinates[bp_ende].append(coordinates[-1])

        # Step 3: Determine a reference coordinate for each station
        logger.info("Calculating reference coordinates for stations...")
        reference_coordinates = {}
        for station, coords in station_coordinates.items():
            # Use the most frequent coordinate
            reference_coordinates[station] = max(set(coords), key=coords.count)

        # Step 4: Normalize geometries
        logger.info("Replacing coordinates in LineString geometries...")
        updated_geometries = []

        for _, row in linie_df.iterrows():
            bp_anfang, bp_ende = row["bp_anfang"], row["bp_ende"]
            coordinates = list(row["geometry"].coords)

            # Replace start and end coordinates with reference values
            coordinates[0] = reference_coordinates[bp_anfang]
            coordinates[-1] = reference_coordinates[bp_ende]

            # Create a new LineString
            updated_geometries.append(LineString(coordinates))

        # Update the GeoDataFrame
        linie_df["geometry"] = updated_geometries

        # Step 5: Save the updated GeoDataFrame as GeoJSON
        logger.info("Saving updated GeoJSON file...")
        linie_df.to_file(output_file, driver="GeoJSON")
        logger.info(f"Updated GeoJSON saved to: {output_file}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    normalize_geometry()
