import folium
import geopandas as gpd

# File path to the GeoJSON file
geojson_file = r"D:/PhD/codingPractices/progress-report-dec-2024/data/processed/swiss/zurich_basel_path.geojson"

# Load the GeoJSON data using GeoPandas
try:
    gdf = gpd.read_file(geojson_file)
    print("GeoJSON data loaded successfully!")
except Exception as e:
    print(f"Error loading GeoJSON: {e}")
    exit()

# Create a map centered on Zurich
if not gdf.empty:
    center_lat = gdf.geometry.centroid.y.mean()
    center_lon = gdf.geometry.centroid.x.mean()
    zurich_basel_map = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    # Add the GeoJSON to the map
    folium.GeoJson(
        gdf,
        name="Zurich to Basel Path",
        style_function=lambda x: {
            "color": "blue",
            "weight": 3,
        },
    ).add_to(zurich_basel_map)

    # Add layer control
    folium.LayerControl().add_to(zurich_basel_map)

    # Save the map to an HTML file
    map_file = r"D:/PhD/codingPractices/progress-report-dec-2024/data/processed/swiss/zurich_basel_map.html"
    zurich_basel_map.save(map_file)
    print(f"Map saved to: {map_file}")

else:
    print("GeoJSON data is empty. No paths to visualize.")
