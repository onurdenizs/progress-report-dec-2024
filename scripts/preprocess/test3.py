import json

# Paths to the input and output GeoJSON files
INPUT_GEOJSON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon.geojson"
OUTPUT_GEOJSON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon_altered.geojson"

def swap_coordinates_for_segment(input_file, output_file, bp_anfang, bp_ende):
    """
    Swap the coordinates of a specified segment and save it to the output file.

    Args:
        input_file (str): Path to the input GeoJSON file.
        output_file (str): Path to the output GeoJSON file.
        bp_anfang (str): Start station of the segment.
        bp_ende (str): End station of the segment.
    """
    try:
        # Load the GeoJSON file
        with open(input_file, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Flag to check if changes were made
        changes_made = False

        # Iterate through the features to find the specified segment
        for feature in geojson_data.get("features", []):
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            
            # Check if the segment matches the specified bp_anfang and bp_ende
            if properties.get("bp_anfang") == bp_anfang and properties.get("bp_ende") == bp_ende:
                if geometry.get("type") == "LineString":
                    coordinates = geometry.get("coordinates", [])
                    if len(coordinates) == 2:
                        # Swap the coordinates
                        coordinates[0], coordinates[1] = coordinates[1], coordinates[0]
                        print(f"Swapped coordinates for segment {bp_anfang} -> {bp_ende}.")
                        changes_made = True
                        break
                else:
                    print(f"Segment {bp_anfang} -> {bp_ende} does not have LineString geometry.")

        if changes_made:
            # Save the altered GeoJSON to the output file
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(geojson_data, f, indent=4)
            print(f"Changes saved to {output_file}")
        else:
            print(f"No changes were made. Segment {bp_anfang} -> {bp_ende} not found or already corrected.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage




swap_coordinates_for_segment(OUTPUT_GEOJSON_FILE, OUTPUT_GEOJSON_FILE, "MISC", "MIRM")
swap_coordinates_for_segment(OUTPUT_GEOJSON_FILE, OUTPUT_GEOJSON_FILE, "MILA", "MIGP")
print("\n\n\nMission Completed")
