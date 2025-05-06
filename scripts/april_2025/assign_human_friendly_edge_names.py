"""
assign_human_friendly_edge_names.py

Phase 1C: Assigns human-readable names to each edge in the railway network,
based on the station names of its from_node and to_node.

Input:
- data/processed/rail_edges.csv
- data/processed/rail_nodes_named.csv

Output:
- data/processed/rail_edges_named.csv

Author: Onur Deniz
Date: 2025-04
"""

import pandas as pd
import logging
import os

# --- Config ---
EDGES_PATH = "data/processed/rail_edges.csv"
NODES_PATH = "data/processed/rail_nodes_named.csv"
OUTPUT_PATH = "data/processed/rail_edges_named.csv"

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def make_station_friendly(name):
    """
    Transforms station name into filename-safe ID fragment.
    E.g., "Zürich HB" -> "Zurich_HB"
    """
    if pd.isna(name):
        return "unknown"
    name = name.replace(" ", "_").replace(",", "").replace("'", "")
    name = name.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    name = name.replace("Ä", "Ae").replace("Ö", "Oe").replace("Ü", "Ue")
    name = name.replace("ß", "ss")
    return name

def main():
    logging.info("🚀 Starting human-readable edge naming...")

    os.makedirs("data/processed", exist_ok=True)

    # --- Load Data ---
    logging.info("📥 Loading edge and node data...")
    edges_df = pd.read_csv(EDGES_PATH)
    nodes_df = pd.read_csv(NODES_PATH)

    logging.info(f"🔗 Edges: {len(edges_df)}, Nodes: {len(nodes_df)}")

    # --- Map Station Names to Nodes ---
    station_lookup = nodes_df.set_index("node_id")["station_name"].to_dict()

    # --- Apply Station Names to Edges ---
    edges_df["from_station"] = edges_df["from_node"].map(station_lookup)
    edges_df["to_station"] = edges_df["to_node"].map(station_lookup)

    # --- Clean Station Names ---
    edges_df["from_clean"] = edges_df["from_station"].apply(make_station_friendly)
    edges_df["to_clean"] = edges_df["to_station"].apply(make_station_friendly)

    # --- Create Edge Name with Index to Avoid Duplicates ---
    edges_df["edge_id_human_base"] = (
        "edge_" + edges_df["from_clean"] + "_" + edges_df["to_clean"]
    )

    # Count occurrences to add suffix for duplicates
    edges_df["edge_id_human"] = edges_df.groupby("edge_id_human_base").cumcount().astype(str).str.zfill(3)
    edges_df["edge_id_human"] = edges_df["edge_id_human_base"] + "_" + edges_df["edge_id_human"]

    # --- Save Result ---
    output_cols = [
        "edge_id", "from_node", "to_node",
        "from_station", "to_station",
        "length", "edge_id_human", "geometry"
    ]
    edges_df[output_cols].to_csv(OUTPUT_PATH, index=False)
    logging.info(f"💾 Saved human-readable edge file: {OUTPUT_PATH}")
    logging.info("✅ Done. Network is now GUI-friendly.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("🔥 Script crashed!", exc_info=True)
