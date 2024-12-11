import folium
import geopandas as gpd
import networkx as nx
from shapely.geometry import LineString

# File path to the GeoJSON dataset
geojson_file = r"D:/PhD/codingPractices/progress-report-dec-2024/data/raw/swiss/linie_mit_polygon/linie_mit_polygon.geojson"

# Define keywords for cities
cities = ["Zurich", "Basel", "Schaffhausen", "Brugg", "Winterthur"]

# Load the GeoJSON data using GeoPandas
try:
    gdf = gpd.read_file(geojson_file)
    print("GeoJSON data loaded successfully!")
except Exception as e:
    print(f"Error loading GeoJSON: {e}")
    exit()

# Filter stations based on city keywords
def filter_stations_by_city(gdf, cities):
    stations = set()
    for city in cities:
        stations.update(gdf[gdf["bp_anf_bez"].str.contains(city, case=False, na=False)]["bp_anf_bez"].unique())
        stations.update(gdf[gdf["bp_end_bez"].str.contains(city, case=False, na=False)]["bp_end_bez"].unique())
    return list(stations)

print("Filtering stations...")
stations = filter_stations_by_city(gdf, cities)
print(f"Stations found: {stations}")

# Create a graph from the GeoDataFrame
print("Building the graph...")
G = nx.Graph()

for _, row in gdf.iterrows():
    start = row["bp_anf_bez"]
    end = row["bp_end_bez"]
    if start and end and isinstance(row["geometry"], LineString):
        G.add_edge(start, end, geometry=row["geometry"])

# Filter stations to those that exist in the graph
print("Checking stations in the graph...")
stations_in_graph = [station for station in stations if station in G.nodes]
missing_stations = [station for station in stations if station not in G.nodes]

print(f"Stations in the graph: {stations_in_graph}")
if missing_stations:
    print(f"Warning: The following stations are not in the graph and will be skipped: {missing_stations}")

# Find all paths between every pair of stations
print("Finding all paths between specified cities...")
all_paths = []
for station_a in stations_in_graph:
    for station_b in stations_in_graph:
        if station_a != station_b and nx.has_path(G, station_a, station_b):
            path = nx.shortest_path(G, station_a, station_b)
            all_paths.append(path)

# Combine paths into a GeoDataFrame for visualization
print("Preparing paths for visualization...")
path_geometries = []
for path in all_paths:
    line_coords = []
    for i in range(len(path) - 1):
        try:
            geom = G[path[i]][path[i + 1]]["geometry"]
            if isinstance(geom, LineString):
                line_coords.extend(list(geom.coords))
        except KeyError:
            continue
    if line_coords:
        path_geometries.append(LineString(line_coords))

paths_gdf = gpd.GeoDataFrame(geometry=path_geometries, crs="EPSG:4326")

# Calculate map center
if not paths_gdf.empty:
    center_lat = paths_gdf.geometry.centroid.y.mean()
    center_lon = paths_gdf.geometry.centroid.x.mean()

    # Create a map centered on Switzerland
    cities_map = folium.Map(location=[center_lat, center_lon], zoom_start=8)

    # Add the GeoJSON paths to the map
    folium.GeoJson(
        paths_gdf,
        name="City Paths",
        style_function=lambda x: {
            "color": "blue",
            "weight": 3,
        },
    ).add_to(cities_map)

    # Add layer control
    folium.LayerControl().add_to(cities_map)

    # Save the map to an HTML file
    map_file = r"D:/PhD/codingPractices/progress-report-dec-2024/data/processed/swiss/city_paths_map.html"
    cities_map.save(map_file)
    print(f"Map saved to: {map_file}")

else:
    print("No paths found to visualize.")

