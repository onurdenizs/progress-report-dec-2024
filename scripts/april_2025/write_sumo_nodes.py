"""
write_sumo_nodes.py

Phase 2: Converts rail_nodes_named.csv to SUMO .nod.xml format.

Input:
- data/processed/rail_nodes_named.csv

Output:
- sumo/inputs/april_2025_swiss/april_2025_swiss.nod.xml
"""

import pandas as pd
import os
import logging
from xml.etree.ElementTree import Element, SubElement, ElementTree

# --- Config ---
INPUT_PATH = "data/processed/rail_nodes_named.csv"
OUTPUT_PATH = "sumo/inputs/april_2025_swiss/april_2025_swiss.nod.xml"

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    logging.info("🚀 Generating SUMO .nod.xml from enriched node file...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    df = pd.read_csv(INPUT_PATH)
    logging.info(f"✅ Loaded {len(df)} nodes from: {INPUT_PATH}")

    # Root XML
    root = Element("nodes")

    for _, row in df.iterrows():
        SubElement(
            root,
            "node",
            id=row["node_id"],
            x=str(row["x"]),
            y=str(row["y"])
        )

    tree = ElementTree(root)
    tree.write(OUTPUT_PATH, encoding="UTF-8", xml_declaration=True)
    logging.info(f"💾 Saved node file to: {OUTPUT_PATH}")
    logging.info("✅ Phase 2 complete. Ready for Phase 3: write_sumo_edges.py")

if __name__ == "__main__":
    main()
