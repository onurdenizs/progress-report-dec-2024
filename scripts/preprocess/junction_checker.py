import xml.etree.ElementTree as ET

# Network file path
NETWORK_FILE = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_comp\sw_real_compV2.net.xml"

# List of junction IDs to check
stations_to_check = ["BS", "BSO", "BSNO", "GELW", "MU", "MUOS", "PRW", "PRUW", "PR", "PRO", "FRE", "LSTN", "LST", "LSN", "IT", "SIS", "GKD", "TK", "HBTN", "HBTS", "OLTU", "OLN", "OL", "OLS", "ABO", "ABOS", "ZFN", "ZF", "BRIT", "REID", "DAG", "NEB", "WAU", "STER", "SSST", "SS", "OBK", "NO", "SEM", "RBG", "RBGD", "HUEB", "GSAG", "EBR", "FMUE", "GTS", "HEIM", "LZEF", "LZ"]

def check_junctions_in_net(network_file, stations):
    """
    Checks if the given station IDs are present as junctions in the SUMO net file.

    Args:
        network_file (str): Path to the SUMO network (.net.xml) file.
        stations (list of str): List of station IDs to check.

    Returns:
        tuple: Two lists - (found_junctions, missing_junctions)
    """
    try:
        # Parse the network file
        tree = ET.parse(network_file)
        root = tree.getroot()

        # Extract all junction IDs from the net file
        junction_ids = {junction.get("id") for junction in root.findall("junction")}

        # Check which stations are found or missing
        found_junctions = [station for station in stations if station in junction_ids]
        missing_junctions = [station for station in stations if station not in junction_ids]

        return found_junctions, missing_junctions

    except Exception as e:
        print(f"Error reading network file: {e}")
        return [], []

def main():
    # Check junctions in the network file
    found, missing = check_junctions_in_net(NETWORK_FILE, stations_to_check)

    # Print results
    print("Found Junctions:")
    print(found)
    print("\nMissing Junctions:")
    print(missing)

if __name__ == "__main__":
    main()
