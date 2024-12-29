import xml.etree.ElementTree as ET

# Absolute paths for the node and edge files
node_file = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_samp\sw_real_samp.nod.xml"
edge_file = r"D:\PhD\codingPractices\progress-report-dec-2024\sumo\inputs\sw_real_samp\sw_real_samp.edge.xml"

# Parse XML files
node_tree = ET.parse(node_file)
edge_tree = ET.parse(edge_file)

# Extract node IDs from the node file
nodes = {node.attrib["id"] for node in node_tree.findall(".//node")}

# Extract edge references from the edge file
edges = edge_tree.findall(".//edge")
missing_nodes = set()

for edge in edges:
    from_node = edge.attrib.get("from")
    to_node = edge.attrib.get("to")
    if from_node not in nodes:
        missing_nodes.add(from_node)
    if to_node not in nodes:
        missing_nodes.add(to_node)

# Output results
if missing_nodes:
    print("Missing nodes:")
    print("\n".join(missing_nodes))
else:
    print("All node references are valid.")
