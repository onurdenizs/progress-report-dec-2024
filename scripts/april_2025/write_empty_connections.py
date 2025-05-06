"""
write_empty_connections.py

Phase 4: Creates an empty placeholder SUMO .con.xml file
required for network compilation with netconvert.

Output:
- sumo/inputs/april_2025_swiss/april_2025_swiss.con.xml
"""

import os
import logging
from xml.etree.ElementTree import Element, ElementTree

# --- Config ---
OUTPUT_PATH = "sumo/inputs/april_2025_swiss/april_2025_swiss.con.xml"

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    logging.info("🧱 Writing empty .con.xml file...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    root = Element("connections")  # No children
    tree = ElementTree(root)
    tree.write(OUTPUT_PATH, encoding="UTF-8", xml_declaration=True)

    logging.info(f"💾 Saved empty connection file to: {OUTPUT_PATH}")
    logging.info("✅ Phase 4 complete. You're now ready for Phase 5: netconvert.")

if __name__ == "__main__":
    main()
