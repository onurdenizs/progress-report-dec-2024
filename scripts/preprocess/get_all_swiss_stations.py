import geopandas as gpd
import pandas as pd
import logging
from pyproj import Transformer
from shapely.geometry import MultiLineString

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# File paths
input_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\normalized_swiss_lines.geojson"
output_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\swiss_stations_normal.csv"

# Transformer for WGS84 to UTM32
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)


def extract_coordinates(row, column, geometry):
    """Extract coordinates based on station abbreviation and geometry."""
    if column == "bp_anfang":
        return list(geometry.geoms[0].coords)[0] if isinstance(geometry, MultiLineString) else list(geometry.coords)[0]
    if column == "bp_ende":
        return list(geometry.geoms[-1].coords)[-1] if isinstance(geometry, MultiLineString) else list(geometry.coords)[-1]
    return None


def main():
    """
    Extract unique Swiss railway stations and their coordinates (WGS84 and UTM).
    Save results to a CSV file.
    """
    try:
        logger.info("Starting extraction of Swiss stations...")

        # Step 1: Load the input GeoJSON file
        linie_df = gpd.read_file(input_file)[["bp_anfang", "bp_ende", "geometry"]]
        logger.info("Input GeoJSON file loaded successfully.")

        # Step 2: Create a DataFrame for unique stations
        swiss_stations = pd.DataFrame(columns=["station", "WGS84"])
        unique_stations = set()

        # Step 3: Traverse through rows to populate swiss_stations
        for _, row in linie_df.iterrows():
            for column in ["bp_anfang", "bp_ende"]:
                station = row[column]
                if station not in unique_stations:
                    unique_stations.add(station)
                    coords = extract_coordinates(row, column, row["geometry"])
                    swiss_stations = pd.concat(
                        [swiss_stations, pd.DataFrame({"station": [station], "WGS84": [coords]})], ignore_index=True
                    )

        logger.info(f"Unique stations extracted: {len(swiss_stations)}")

        # Step 4: Add UTM coordinates
        swiss_stations["UTM"] = swiss_stations["WGS84"].apply(
            lambda coord: transformer.transform(coord[0], coord[1])
        )
        logger.info("UTM coordinates added successfully.")

        # Step 5: Validate uniqueness
        duplicates_wgs84 = swiss_stations[swiss_stations.duplicated(subset="WGS84", keep=False)]
        duplicates_utm = swiss_stations[swiss_stations.duplicated(subset="UTM", keep=False)]

        if not duplicates_wgs84.empty:
            logger.warning("Stations with duplicate WGS84 coordinates:")
            logger.warning(duplicates_wgs84["station"].tolist())

        if not duplicates_utm.empty:
            logger.warning("Stations with duplicate UTM coordinates:")
            logger.warning(duplicates_utm["station"].tolist())

        # Step 6: Log total number of stations and save to CSV
        logger.info(f"Total number of stations created: {len(swiss_stations)}")
        swiss_stations.to_csv(output_file, index=False)
        logger.info(f"Swiss stations saved to {output_file}")

    except Exception as e:
        logger.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
