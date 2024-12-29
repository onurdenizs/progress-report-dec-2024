import xml.etree.ElementTree as ET

# Path to the network file
NETWORK_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_compV2.net.xml"

# List of station pairs
stations = ['BSO', 'BSNO', 'GELW', 'MU', 'MUOS', 'PRW', 'PRUW', 'PRO', 'LSTN', 'LST', 'SIS', 'OLN', 'OL', 'OLS', 'ABO', 'ABOS', 'ZFN', 'SSST', 'HUEB', 'FMUE', 'GTS', 'LZEF', 'LZ']

def check_edges_between_stations(network_file, stations):
    """
    Checks if edges exist between consecutive station pairs in the provided list
    and returns a list of found edges and their IDs.
    """
    edge_ids_found = []
    missing_edges = []

    try:
        tree = ET.parse(network_file)
        root = tree.getroot()

        for i in range(len(stations) - 1):
            from_station = stations[i]
            to_station = stations[i + 1]
            edge_id = None

            for edge in root.findall("edge"):
                if edge.get("from") == from_station and edge.get("to") == to_station:
                    edge_id = edge.get("id")
                    edge_ids_found.append(edge_id)
                    break

            if edge_id:
                print(f"Edge from {from_station} to {to_station} (ID: {edge_id}) found.")
            else:
                missing_edges.append((from_station, to_station))
                print(f"Edge from {from_station} to {to_station} is missing.")

    except Exception as e:
        print(f"An error occurred: {e}")

    return edge_ids_found, missing_edges

def main():
    edge_ids, missing = check_edges_between_stations(NETWORK_FILE, stations)

    print("\nEdge IDs Found:")
    print(edge_ids)

    print("\nMissing Edges:")
    for edge in missing:
        print(f"From {edge[0]} to {edge[1]}")

    # Save the list of found edges to a file (optional)
    output_file = r"D:\PhD\codingPractices\progress-report-dec-2024\found_edges.txt"
    with open(output_file, "w") as f:
        f.write(" ".join(edge_ids))
    print(f"\nEdge IDs saved to {output_file}")

if __name__ == "__main__":
    main()
