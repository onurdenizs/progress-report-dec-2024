"""
generate_net_with_netconvert.py

Phase 5: Runs SUMO's netconvert tool to compile the network
from .nod.xml, .edg.xml, and .con.xml into a .net.xml.

Input:
- april_2025_swiss.nod.xml
- april_2025_swiss.edg.xml
- april_2025_swiss.con.xml

Output:
- april_2025_swiss.net.xml
"""

import os
import subprocess
import logging

# --- Config ---
SUMO_BIN = "netconvert"  # Ensure this is in your PATH
INPUT_DIR = "sumo/inputs/april_2025_swiss/"
OUTPUT_FILE = os.path.join(INPUT_DIR, "april_2025_swiss.net.xml")

# --- Logging ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def main():
    logging.info("🔧 Running netconvert to generate .net.xml...")

    cmd = [
        SUMO_BIN,
        f"--node-files={os.path.join(INPUT_DIR, 'april_2025_swiss.nod.xml')}",
        f"--edge-files={os.path.join(INPUT_DIR, 'april_2025_swiss.edg.xml')}",
        f"--connection-files={os.path.join(INPUT_DIR, 'april_2025_swiss.con.xml')}",
        f"--output-file={OUTPUT_FILE}",
        "--no-turnarounds"  # This is valid for rail-style networks
    ]

    logging.info("🔧 Executing:")
    logging.info(" ".join(cmd))

    try:
        subprocess.run(cmd, check=True)
        logging.info(f"✅ Network generated: {OUTPUT_FILE}")
        logging.info("🎉 Phase 5 complete. Ready to inspect in SUMO-GUI or run validation.")
    except subprocess.CalledProcessError as e:
        logging.error("❌ netconvert failed!", exc_info=True)

if __name__ == "__main__":
    main()
