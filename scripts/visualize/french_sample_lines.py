import geopandas as gpd
import folium
import os
from shapely.geometry import LineString, MultiLineString

def extract_coordinates(line_id, vitesse_data):
    """Extracts the starting coordinates for a line based on the smallest pkd value.

    Args:
        line_id (str): The ID of the line to filter.
        vitesse_data (GeoDataFrame): The vitesse_maximale GeoDataFrame.

    Returns:
        tuple: A tuple containing the latitude and longitude of the starting coordinate.
    """
    filtered_data = vitesse_data[vitesse_data['code_ligne'] == line_id].copy()

    def convert_pkd(pkd):
        """Converts pkd value from string to numeric format."""
        if '+' in pkd:
            main, sub = pkd.split('+')
            return float(main) + float(sub) / 1000
        return float(pkd)

    filtered_data['pkd'] = filtered_data['pkd'].apply(convert_pkd)
    filtered_data = filtered_data[filtered_data['geometry'].notnull()]  # Filter valid geometries
    first_segment = filtered_data.sort_values(by='pkd').iloc[0]

    if isinstance(first_segment.geometry, LineString):
        return first_segment.geometry.coords[0][1], first_segment.geometry.coords[0][0]
    elif isinstance(first_segment.geometry, MultiLineString):
        first_line = list(first_segment.geometry.geoms)[0]
        return first_line.coords[0][1], first_line.coords[0][0]

def filter_station_uic(station_uic, gares_data):
    """Filters station data to find the entry containing a specific UIC code.

    Args:
        station_uic (str): The UIC code to search for.
        gares_data (GeoDataFrame): The gares GeoDataFrame.

    Returns:
        GeoSeries or None: The filtered station row, or None if not found.
    """
    print(f"Searching for UIC: {station_uic}")
    filtered = gares_data[gares_data['codes_uic'].str.contains(station_uic, na=False)]
    if filtered.empty:
        print(f"Warning: UIC {station_uic} not found in dataset.")
        return None
    return filtered.iloc[0]

def draw_line_segments(line_id, lines_data, map_object, style):
    """Draws line segments for a specific railway line on the map.

    Args:
        line_id (str): The ID of the railway line to draw.
        lines_data (GeoDataFrame): The vitesse_maximale GeoDataFrame.
        map_object (folium.Map): The folium map object.
        style (dict): Dictionary containing style properties for the line.

    Returns:
        None
    """
    line_segments = lines_data[(lines_data['code_ligne'] == line_id) & 
                               (lines_data['geometry'].notnull())]  # Filter valid geometries

    for _, segment in line_segments.iterrows():
        if isinstance(segment.geometry, LineString):
            points = [(coord[1], coord[0]) for coord in segment.geometry.coords]
            folium.PolyLine(
                points, color=style['color'], dash_array=style['dash_array'], weight=2
            ).add_to(map_object)
        elif isinstance(segment.geometry, MultiLineString):
            for line in segment.geometry.geoms:
                points = [(coord[1], coord[0]) for coord in line.coords]
                folium.PolyLine(
                    points, color=style['color'], dash_array=style['dash_array'], weight=2
                ).add_to(map_object)
        else:
            print(f"Skipping unsupported geometry in line {line_id}, segment ID: {segment.get('idgaia', 'Unknown')}.")

def create_map(lines_data, gares_data, output_path):
    """Creates an interactive map with specified railway lines and stations.

    Args:
        lines_data (GeoDataFrame): The vitesse_maximale GeoDataFrame.
        gares_data (GeoDataFrame): The gares GeoDataFrame.
        output_path (str): The path to save the output map.

    Returns:
        None
    """
    print("Creating folium map...")
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

    line_styles = {
        '001000': {'color': 'blue', 'dash_array': '5, 5'},
        '420000': {'color': 'green', 'dash_array': '1, 6'},
        '830000': {'color': 'red', 'dash_array': None},
    }

    line_stations = {
        '001000': [
            {'name': "Paris L'est", 'uic': None, 'coords': extract_coordinates('001000', lines_data)},
            {'name': 'Belfort', 'uic': '87184002'},  # Corrected UIC
            {'name': 'Mulhouse', 'uic': '87182063'},
        ],
        '420000': [
            {'name': 'Paris-Montparnasse', 'uic': '87391003'},
            {'name': 'Rennes', 'uic': '87471003'},
            {'name': 'Lamballe', 'uic': '87473108'},
            {'name': 'Guingamp', 'uic': '87473207'},
            {'name': 'Plouret-Tregor', 'uic': '87473181'},
            {'name': 'Morlaix', 'uic': '87474338'},
            {'name': 'Brest', 'uic': '87474007'},
        ],
        '830000': [
            {'name': 'Paris gare de Lyon', 'uic': '87686006'},
            {'name': 'Avignon', 'uic': '87765008'},
            {'name': 'Marseille', 'uic': '87751008'},
        ],
    }

    for line_id, style in line_styles.items():
        draw_line_segments(line_id, lines_data, m, style)

    for line_id, stations in line_stations.items():
        style = line_styles[line_id]
        for station in stations:
            if station['uic']:
                station_data = filter_station_uic(station['uic'], gares_data)
                if station_data is None:
                    continue
                coords = (station_data.geometry.y, station_data.geometry.x)
            else:
                coords = station['coords']

            folium.Marker(
                coords, popup=station['name'],
                icon=folium.Icon(color=style['color'])
            ).add_to(m)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    print(f"Directory created: {os.path.dirname(output_path)}")
    m.save(output_path)
    print(f"Map saved at: {output_path}")

if __name__ == "__main__":
    gares_path = r"D:\\PhD\\codingPractices\\progress-report-dec-2024\\data\\raw\\french\\gares\\gares.geojson"
    vitesse_path = r"D:\\PhD\\codingPractices\\progress-report-dec-2024\\data\\raw\\french\\vitesse_maximale\\vitesse_maximale.geojson"

    gares = gpd.read_file(gares_path)
    vitesse = gpd.read_file(vitesse_path)

    output_map_path = r"D:\\PhD\\codingPractices\\progress-report-dec-2024\\outputs\\visualizations\\french\\selected_french_lines.html"

    create_map(vitesse, gares, output_map_path)
