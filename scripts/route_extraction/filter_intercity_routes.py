import pandas as pd
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# === Config ===
GTFS_ROUTES_FILE = Path("data/raw/swiss/gtfs_ftp_2025/routes.txt")
OUTPUT_FILE = Path("data/processed/routes/intercity_route_candidates.csv")

# Keywords that suggest inter-city lines in route_short_name
INTERCITY_KEYWORDS = ["IC", "IR", "RE"]

def main():
    logging.info(f"📂 Loading GTFS routes from {GTFS_ROUTES_FILE}")
    df = pd.read_csv(GTFS_ROUTES_FILE)

    # Normalize the route_short_name
    df["route_short_name"] = df["route_short_name"].astype(str).str.upper()

    # Filter based on substrings in route_short_name
    mask = df["route_short_name"].apply(lambda x: any(kw in x for kw in INTERCITY_KEYWORDS))
    df_intercity = df[mask].copy()

    logging.info(f"✅ Found {len(df_intercity)} likely inter-city routes based on short_name")
    logging.info("\n📊 Inter-city route candidates:")
    logging.info(df_intercity[["route_id", "route_short_name", "route_long_name"]].head(15).to_string(index=False))

    logging.info(f"📅 Saving filtered inter-city routes to {OUTPUT_FILE}")
    df_intercity.to_csv(OUTPUT_FILE, index=False)
    logging.info("✅ Done.")

if __name__ == "__main__":
    main()
