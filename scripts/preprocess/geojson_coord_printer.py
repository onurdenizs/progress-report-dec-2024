import json

# Constant defining the path to the GeoJSON file
INPUT_GEOJSON_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon_altered.geojson"

def get_segment_coordinates(input_file, bp_anfang, bp_ende):
    """
    Reads the GeoJSON file and prints the coordinates of the segment matching bp_anfang and bp_ende.

    Args:
        input_file (str): Path to the GeoJSON file.
        bp_anfang (str): Start station of the segment.
        bp_ende (str): End station of the segment.
    """
    try:
        # Load the GeoJSON file
        with open(input_file, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)

        # Search for the segment with matching bp_anfang and bp_ende
        for feature in geojson_data.get("features", []):
            properties = feature.get("properties", {})
            geometry = feature.get("geometry", {})
            
            if properties.get("bp_anfang") == bp_anfang and properties.get("bp_ende") == bp_ende:
                if geometry.get("type") == "LineString":
                    coordinates = geometry.get("coordinates", [])
                    print(f"{bp_anfang} - {bp_ende}")
                    print(coordinates)
                    return
                else:
                    print(f"Segment {bp_anfang} -> {bp_ende} does not have LineString geometry.")
                    return
        
        print(f"Segment {bp_anfang} -> {bp_ende} not found in the GeoJSON file.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get user input for bp_anfang and bp_ende
    bp_anfang = "STNE"
    bp_ende = "MLG"

    # Call the function to get segment coordinates
    # get_segment_coordinates(INPUT_GEOJSON_FILE, bp_anfang, bp_ende)
    
   
    get_segment_coordinates(INPUT_GEOJSON_FILE, "BS", "BSO")
 
    
   