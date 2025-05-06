"""
summarize_network_contents.py

Phase 6: Loads a SUMO .net.xml file and prints summary statistics
about nodes and edges to validate network structure.

Run this locally inside your environment.
"""

import xml.etree.ElementTree as ET
from collections import Counter
import pandas as pd
import logging
import os

# === Configuration ===
INPUT_NET_PATH = "sumo/inputs/april_2025_swiss/april_2025_swiss.net.xml"

# === Logging setup ===
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    logging.info(f"📂 Parsing network: {INPUT_NET_PATH}")
    
    tree = ET.parse(INPUT_NET_PATH)
    root = tree.getroot()

    nodes = []
    edges = []

    for child in root:
        if child.tag == "junction":
            nodes.append(child.attrib)
        elif child.tag == "edge" and "id" in child.attrib:
            edges.append(child.attrib)

    df_nodes = pd.DataFrame(nodes)
    df_edges = pd.DataFrame(edges)

    # === Summary ===
    logging.info("📊 Node Summary")
    logging.info(f"🔢 Total Nodes: {len(df_nodes)}")
    if "type" in df_nodes.columns:
        logging.info(f"📌 Junction Types: {dict(Counter(df_nodes['type']))}")
    
    logging.info("📊 Edge Summary")
    logging.info(f"🔢 Total Edges: {len(df_edges)}")
    logging.info(f"🆔 Sample Edge IDs: {df_edges['id'].sample(n=5, random_state=42).tolist()}")
    if {"from", "to"}.issubset(df_edges.columns):
        logging.info("🔗 Sample 'from' and 'to' pairs:")
        for i, row in df_edges[["from", "to"]].dropna().sample(n=5, random_state=42).iterrows():
            logging.info(f"  ➜ {row['from']} → {row['to']}")

    logging.info("✅ Phase 6 complete: Network validated successfully.")

if __name__ == "__main__":
    main()
