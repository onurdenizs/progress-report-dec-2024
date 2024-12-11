import geopandas as gpd

# Path to the GeoJSON file
geojson_file = r"D:/PhD/codingPractices/progress-report-dec-2024/data/processed/swiss/zurich_basel_path.geojson"

# Load and inspect the dataset
try:
    gdf = gpd.read_file(geojson_file)
    print("Dataset loaded successfully!")
    print("Columns in the dataset:")
    print(gdf.columns)

    # Check for `bp_anf_bez` and `bp_end_bez`
    if "bp_anf_bez" in gdf.columns and "bp_end_bez" in gdf.columns:
        print("Columns 'bp_anf_bez' and 'bp_end_bez' are present.")
    else:
        print("Required columns 'bp_anf_bez' or 'bp_end_bez' are missing.")
except Exception as e:
    print(f"Error: {e}")
