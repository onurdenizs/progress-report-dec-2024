import pandas as pd
from pathlib import Path

ROUTES_FILE = Path("data/raw/swiss/gtfs_ftp_2025/routes.txt")

df = pd.read_csv(ROUTES_FILE)

print("🧩 Unique route_type values:")
print(df["route_type"].value_counts())

print("\n🧩 Sample route_short_name values:")
print(df["route_short_name"].dropna().unique()[:50])  # First 50 non-null names
