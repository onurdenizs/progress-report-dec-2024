import pandas as pd
import xml.etree.ElementTree as ET
from pathlib import Path
import logging

# ─── Setup Logging ─────────────────────────────────────────────────────────────
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# ─── File Paths ────────────────────────────────────────────────────────────────
INPUT_CSV = Path("data/processed/routes/selected_intercity_routes.csv")
OUTPUT_XML = Path("data/processed/routes/selected_intercity_routes.rou.xml")

# ─── Helper Functions ──────────────────────────────────────────────────────────
def sanitize_stop_id(stop_id: str) -> str:
    """Convert stop_id to a format valid for SUMO edge IDs."""
    return stop_id.replace(":", "_").replace("/", "_")

def generate_trip_elements(df: pd.DataFrame) -> list:
    """
    Generate SUMO <trip> XML elements from GTFS route data.

    Args:
        df (pd.DataFrame): Filtered GTFS trip-stop data.

    Returns:
        List of ElementTree <trip> elements.
    """
    trips = []
    grouped = df.groupby("trip_id")

    for trip_id, group in grouped:
        group_sorted = group.sort_values("stop_sequence")
        route_id = group_sorted["route_id"].iloc[0]
        departure_time = group_sorted["departure_time"].iloc[0]  # First departure time

        # Convert HH:MM:SS to seconds since midnight
        h, m, s = map(int, departure_time.split(":"))
        depart_seconds = h * 3600 + m * 60 + s

        # Generate route by concatenating sanitized stop_ids
        route_edges = " ".join(sanitize_stop_id(sid) for sid in group_sorted["stop_id"])

        trip_elem = ET.Element("trip", attrib={
            "id": trip_id,
            "depart": str(depart_seconds),
            "from": sanitize_stop_id(group_sorted["stop_id"].iloc[0]),
            "to": sanitize_stop_id(group_sorted["stop_id"].iloc[-1]),
            "route": route_edges
        })
        trips.append(trip_elem)

    return trips

# ─── Main Logic ────────────────────────────────────────────────────────────────
def main():
    logging.info(f"📂 Reading GTFS data from {INPUT_CSV}")
    df = pd.read_csv(INPUT_CSV)

    logging.info("🛠 Generating SUMO trip definitions...")
    trips = generate_trip_elements(df)

    logging.info(f"💾 Writing to {OUTPUT_XML}")
    root = ET.Element("routes")
    for trip_elem in trips:
        root.append(trip_elem)

    tree = ET.ElementTree(root)
    OUTPUT_XML.parent.mkdir(parents=True, exist_ok=True)
    tree.write(OUTPUT_XML, encoding="utf-8", xml_declaration=True)
    logging.info("✅ .rou.xml file written successfully.")

if __name__ == "__main__":
    main()
