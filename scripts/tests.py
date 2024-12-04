import geopandas as gpd
import networkx as nx

# File path
input_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/raw/sbbs_route_network/sbbs_route_network.geojson"

def load_dataset(filepath):
    """Load the GeoJSON dataset."""
    print(f"Loading dataset from {filepath}...")
    gdf = gpd.read_file(filepath)
    print("Dataset loaded successfully!")
    return gdf

def build_graph(gdf):
    """Build a graph representation of the dataset."""
    print("Building graph from dataset...")
    G = nx.Graph()
    for _, row in gdf.iterrows():
        G.add_edge(row['bpk_anfang'], row['bpk_ende'], linie=row['linie'])
    print("Graph built successfully!")
    return G

def find_path(G, start, end):
    """Find all line segments forming the path between two stations."""
    try:
        print(f"Finding path from {start} to {end}...")
        path = nx.shortest_path(G, source=start, target=end)
        print("Path found successfully!")
        return path
    except nx.NetworkXNoPath:
        print(f"No path found between {start} and {end}.")
        return []
    except nx.NodeNotFound as e:
        print(f"Error: {e}")
        return []

def get_path_segments(gdf, path):
    """Extract line segments forming the path."""
    print("Extracting line segments for the path...")
    path_segments = []
    for i in range(len(path) - 1):
        segment = gdf[
            (gdf['bpk_anfang'] == path[i]) & (gdf['bpk_ende'] == path[i + 1])
        ]
        if not segment.empty:
            path_segments.append(segment)
    print(f"{len(path_segments)} segments found.")
    return gpd.GeoDataFrame(pd.concat(path_segments), crs=gdf.crs)

def main():
    # Load dataset
    gdf = load_dataset(input_file)

    # Build graph
    G = build_graph(gdf)

    # Define start and end stations
    start_station = "Lausanne"
    end_station = "Zurich"

    # Find path
    path = find_path(G, start_station, end_station)

    if path:
        print(f"Path: {' -> '.join(path)}")
        # Extract segments
        path_segments = get_path_segments(gdf, path)

        # Save results
        output_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/processed/path_segments.geojson"
        path_segments.to_file(output_file, driver="GeoJSON")
        print(f"Path segments saved to {output_file}")
    else:
        print("No valid path found.")

if __name__ == "__main__":
    main()
