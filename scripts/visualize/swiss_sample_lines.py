"""
Visualize specific railway lines and stations on an interactive map.

This script selects segments from lines 500, 660, and 720 to create a visual representation
of train journeys from Basel SBB to Luzern and Luzern to Zürich Langstrasse, highlighting
specific stations and routes. The output is an interactive HTML map.

Input:
- GeoJSON file containing railway line data.

Output:
- Interactive HTML map showing the selected railway lines and stations.

Author: Your Name
"""

import folium
import geopandas as gpd


def filter_segments(data, line_number, start_end_pairs=None):
    """
    Filters railway line segments based on line number and optionally specific start-end pairs.

    Args:
        data (GeoDataFrame): The input GeoDataFrame containing line data.
        line_number (int): The railway line number to filter.
        start_end_pairs (list of tuple, optional): List of specific (start, end) station pairs
            to include. If None, filters only by line number.

    Returns:
        GeoDataFrame: Filtered GeoDataFrame containing the desired segments.
    """
    if start_end_pairs:
        return data[
            (data['linienr'] == line_number) &
            (
                data.apply(
                    lambda row: (row['bp_anf_bez'], row['bp_end_bez']) in start_end_pairs or
                                (row['bp_end_bez'], row['bp_anf_bez']) in start_end_pairs,
                    axis=1
                )
            )
        ]
    return data[data['linienr'] == line_number]


def add_segments_to_map(map_object, segments, color, weight=3):
    """
    Adds railway line segments to a folium map.

    Args:
        map_object (folium.Map): The folium map object to update.
        segments (GeoDataFrame): GeoDataFrame containing the line segments.
        color (str): Color of the line segments.
        weight (int, optional): Thickness of the line segments. Defaults to 3.
    """
    folium.GeoJson(
        segments,
        style_function=lambda _: {"color": color, "weight": weight},
    ).add_to(map_object)


def add_stations_to_map(map_object, stations, color="red"):
    """
    Adds station markers to a folium map.

    Args:
        map_object (folium.Map): The folium map object to update.
        stations (list of dict): List of stations with name, latitude, and longitude.
        color (str, optional): Marker color. Defaults to "red".
    """
    for station in stations:
        folium.Marker(
            location=[station['lat'], station['lon']],
            popup=station['name'],
            icon=folium.Icon(color=color),
        ).add_to(map_object)


def main():
    """
    Main function to visualize selected railway lines and stations on an interactive map.
    """
    # Input GeoJSON file
    input_file = r"D:/PhD/codingPractices/progress-report-dec-2024/data/raw/swiss/linie_mit_polygon/linie_mit_polygon.geojson"

    # Output HTML file
    output_html = r"D:/PhD/codingPractices/progress-report-dec-2024/outputs/visualizations/swiss/swiss_sample.html"

    # Load the GeoJSON file
    gdf = gpd.read_file(input_file)
    print("GeoJSON data loaded successfully!")

    # Define segments for lines 500, 660, and 720
    line_500_segments = filter_segments(gdf, 500)
    line_660_segments = filter_segments(gdf, 660)
    line_720_segments_list = [
        ("Thalwil Nord (Abzw)", "Thalwil"),
        ("Rüschlikon", "Thalwil Nord (Abzw)"),
        ("Kilchberg ZH", "Rüschlikon"),
        ("Zürich Wollishofen", "Kilchberg ZH"),
        ("Zürich Enge", "Zürich Wollishofen"),
        ("Zürich Wiedikon", "Zürich Enge"),
        ("Zürich Lochergut (Abzw)", "Zürich Wiedikon"),
        ("Zürich Aussersihl (Abzw)", "Zürich Lochergut (Abzw)"),
        ("Zürich Langstrasse", "Zürich Aussersihl (Abzw)"),
    ]
    line_720_segments = filter_segments(gdf, 720, line_720_segments_list)

    # Define stations
    stations = [
        {"name": "Basel SBB", "lat": 47.547, "lon": 7.589},
        {"name": "Liestal", "lat": 47.486, "lon": 7.734},
        {"name": "Sissach", "lat": 47.462, "lon": 7.810},
        {"name": "Gelterkinden", "lat": 47.463, "lon": 7.857},
        {"name": "Olten", "lat": 47.352, "lon": 7.903},
        {"name": "Zofingen", "lat": 47.287, "lon": 7.946},
        {"name": "Sursee", "lat": 47.171, "lon": 8.100},
        {"name": "Luzern", "lat": 47.049, "lon": 8.308},
        {"name": "Rotkreuz", "lat": 47.141, "lon": 8.431},
        {"name": "Zug Nord (Abzw)", "lat": 47.183, "lon": 8.515},
        {"name": "Baar", "lat": 47.195, "lon": 8.532},
        {"name": "Thalwil", "lat": 47.292, "lon": 8.563},
        {"name": "Zürich Langstrasse", "lat": 47.378, "lon": 8.527},
    ]

    # Initialize the map centered on Luzern
    center_coords = [47.049, 8.308]
    swiss_map = folium.Map(location=center_coords, zoom_start=9)

    # Add segments and stations to the map
    add_segments_to_map(swiss_map, line_500_segments, "blue")
    add_segments_to_map(swiss_map, line_660_segments, "green")
    add_segments_to_map(swiss_map, line_720_segments, "orange")
    add_stations_to_map(swiss_map, stations, "red")

    # Save the interactive map to an HTML file
    swiss_map.save(output_html)
    print(f"Interactive map saved to: {output_html}")


if __name__ == "__main__":
    main()
