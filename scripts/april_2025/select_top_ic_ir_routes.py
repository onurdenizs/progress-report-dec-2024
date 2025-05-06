"""
select_top_ic_ir_routes.py

Purpose:
Filter and display top IC (InterCity) and IR (InterRegio) routes from cleaned_routes_summary.csv
for manual selection of high-traffic simulation candidates.

Input:
- data/processed/routes/cleaned_routes_summary.csv

Output:
- Console preview of IC and IR route candidates with trip count and station names.
"""

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

FILE_PATH = "data/processed/routes/cleaned_routes_summary.csv"

def main():
    logging.info(f"📥 Loading: {FILE_PATH}")
    df = pd.read_csv(FILE_PATH)

    logging.info("🔍 Filtering IC and IR routes...")
    df_ic = df[df["route_short_name"].str.contains(r"\bIC\b", case=False, na=False)].copy()
    df_ir = df[df["route_short_name"].str.contains(r"\bIR\b", case=False, na=False)].copy()

    logging.info(f"✅ Found {len(df_ic)} IC routes and {len(df_ir)} IR routes.")
    
    logging.info("📊 Top 10 IC routes by trip_count:")
    print(df_ic.sort_values("trip_count", ascending=False).head(10)[
        ["route_id", "trip_headsign", "route_short_name", "trip_count"]
    ])

    logging.info("📊 Top 10 IR routes by trip_count:")
    print(df_ir.sort_values("trip_count", ascending=False).head(10)[
        ["route_id", "trip_headsign", "route_short_name", "trip_count"]
    ])

if __name__ == "__main__":
    main()
