import os
import logging
from lxml import etree

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)-8s %(message)s")

# Paths
OUTPUT_FILE = os.path.join("data", "processed", "rail_connections.con.xml")

# Start XML structure
root = etree.Element("connections")

# Write to file
tree = etree.ElementTree(root)
tree.write(OUTPUT_FILE, pretty_print=True, xml_declaration=True, encoding="UTF-8")

logging.info("💾 Wrote empty connection file to %s", OUTPUT_FILE)
logging.info("✅ Phase 5 complete")
