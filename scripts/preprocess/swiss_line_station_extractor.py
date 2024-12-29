import os
import csv
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Input GeoJSON file path
INPUT_GEOJSON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon.geojson"
OUTPUT_CSV_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\swiss_linienr_stations.csv"

# Example input parameters
LINIENR = 500
KNOWN_STATIONS = ["BS", "LZ"]  # Provide only the first and last station

def load_geojson(file_path):
    """Load GeoJSON data from a file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load GeoJSON file: {e}")
        raise

def filter_segments_by_linenr(features, linienr):
    """Filter segments by linienr."""
    return [feature for feature in features if feature["properties"]["linienr"] == linienr]

def extract_ordered_stations(segments, known_stations):
    """
    Extract ordered stations for the given linienr by traversing line segments.

    Args:
        segments (list): Filtered GeoJSON features for the linienr.
        known_stations (list): List containing the origin and destination stations.

    Returns:
        list: Ordered list of stations for the linienr, formatted for direct use in VEHICLE_ROUTES.
    """
    origin = known_stations[0]
    destination = known_stations[-1]

    # Initialize traversal
    current_station = origin
    ordered_stations = [current_station]
    remaining_segments = segments.copy()

    while current_station != destination:
        # Find the next segment starting from the current station
        next_segment = next(
            (seg for seg in remaining_segments if seg["properties"]["bp_anfang"] == current_station),
            None
        )

        if not next_segment:
            raise ValueError(f"No next segment found starting from {current_station}. Check data consistency.")

        # Add the ending station of the found segment
        next_station = next_segment["properties"]["bp_ende"]
        ordered_stations.append(next_station)

        # Update current station and remove the used segment
        current_station = next_station
        remaining_segments.remove(next_segment)

    # Format for direct use in VEHICLE_ROUTES
    return [f'"{station}"' for station in ordered_stations]

def save_stations_to_csv(linienr, ordered_stations, output_file):
    """
    Save the ordered stations to a CSV file.

    Args:
        linienr (int): The linienr for which the stations are extracted.
        ordered_stations (list): List of ordered stations.
        output_file (str): Path to the output CSV file.
    """
    try:
        formatted_stations = ", ".join(ordered_stations)
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["linienr", "stations"])
            writer.writerow([linienr, formatted_stations])  # Write formatted string to CSV
        logger.info(f"Ordered stations saved to {output_file}")
    except Exception as e:
        logger.error(f"Failed to save ordered stations to CSV: {e}")
        raise

def main(linienr, known_stations):
    """
    Main function to extract ordered stations for a given linienr and save to a CSV.

    Args:
        linienr (int): The linienr to process.
        known_stations (list): List containing the origin and destination stations.
    """
    logger.info("Loading input GeoJSON file...")
    data = load_geojson(INPUT_GEOJSON_FILE)
    features = data.get("features", [])
    logger.info("Input file loaded successfully.")

    logger.info(f"Filtering segments for linienr={linienr}...")
    filtered_segments = filter_segments_by_linenr(features, linienr)
    if not filtered_segments:
        raise ValueError(f"No segments found for linienr={linienr}")

    logger.info("Extracting ordered stations...")
    ordered_stations = extract_ordered_stations(filtered_segments, known_stations)
    ordered_stations_str = ", ".join(ordered_stations)
    logger.info(f"Ordered stations: {ordered_stations_str}")

    logger.info("Saving ordered stations to CSV...")
    save_stations_to_csv(linienr, ordered_stations, OUTPUT_CSV_FILE)

if __name__ == "__main__":
    main(LINIENR, KNOWN_STATIONS)
