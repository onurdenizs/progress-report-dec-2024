import geopandas as gpd
import networkx as nx
import os

# File paths
input_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/raw/swiss/linie_mit_polygon/linie_mit_polygon.geojson"
output_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/processed/swiss/zurich_basel_path.geojson"

# Define Zurich and Basel stations
zurich_stations = [
    'Zürich, Rehalp', 'Zürich Seebach Ost (Abzw)', 'Zürich Langstrasse', 'Zürich HB',
    'Zürich Altstetten', 'Zürich Hardbrücke West (Spw)', 'Zürich Stadelhofen', 'Zürich Flughafen'
]
basel_stations = [
    'Basel Werkstätte Hardacker', 'Basel SBB', 'Basel Bad Bf', 'Basel SBB Tiefbahnhof',
    'Basel Kleinhüningen Hafen', 'Basel Auhafen'
]

# Load the GeoJSON file
print("Loading the dataset...")
gdf = gpd.read_file(input_file)
print("Dataset successfully loaded!")

# Normalize column names
gdf.columns = gdf.columns.str.strip().str.lower()

# Normalize station names
gdf["bp_anf_bez"] = gdf["bp_anf_bez"].str.strip()
gdf["bp_end_bez"] = gdf["bp_end_bez"].str.strip()

# Create the graph
print("Building the graph...")
G = nx.DiGraph()  # Using a directed graph

# Add nodes and edges
nodes_added = set()
for _, row in gdf.iterrows():
    start = row["bp_anf_bez"]
    end = row["bp_end_bez"]
    geometry = row["geometry"]  # Use the correct geometry column

    if geometry is None:
        print(f"Missing geometry information: {start} -> {end}")
        continue

    G.add_edge(start, end, geometry=geometry)
    nodes_added.update([start, end])

print(f"{len(nodes_added)} nodes added to the graph.")

# Check if Zurich and Basel stations exist in the graph
missing_zurich_stations = [station for station in zurich_stations if station not in nodes_added]
missing_basel_stations = [station for station in basel_stations if station not in nodes_added]

if missing_zurich_stations:
    print("Missing Zurich stations in the graph:", missing_zurich_stations)
if missing_basel_stations:
    print("Missing Basel stations in the graph:", missing_basel_stations)

# Find paths between Zurich and Basel
print("Searching for paths between Zurich and Basel...")
paths = []
for zurich_station in zurich_stations:
    for basel_station in basel_stations:
        if nx.has_path(G, zurich_station, basel_station):
            path = nx.shortest_path(G, source=zurich_station, target=basel_station)
            paths.append(path)

if paths:
    print(f"{len(paths)} paths found. Processing the first path...")
    selected_path = paths[0]
    segments = []

    # Retrieve geometry for each segment in the selected path
    for i in range(len(selected_path) - 1):
        edge_data = G.get_edge_data(selected_path[i], selected_path[i + 1])
        segments.append(edge_data["geometry"])

    # Create GeoDataFrame and save it
    path_gdf = gpd.GeoDataFrame({"geometry": segments})
    path_gdf.set_crs(gdf.crs, inplace=True)  # Ensure CRS is preserved
    path_gdf.to_file(output_file, driver="GeoJSON")
    print(f"Path between Zurich and Basel saved to: {output_file}")
else:
    print("No path found between Zurich and Basel.")
