import fiona
import geopandas as gpd

data_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\swissTNE_Base_20240507.gpkg"

print("📂 Available layers:")
layers = fiona.listlayers(data_file)
for layer in layers:
    print(f"  - {layer}")

for layer in layers:
    print(f"\n--- Analyzing layer: {layer} ---")
    gdf = gpd.read_file(data_file, layer=layer)
    print(f"✅ {layer} - {len(gdf)} rows")
    print("📌 Columns:", list(gdf.columns))

    # Only check geometry type if it's a GeoDataFrame (has 'geometry' column)
    if "geometry" in gdf.columns:
        print("📐 Geometry type:", gdf.geom_type.unique())
        print(gdf.head(3))
    else:
        print("ℹ️ No geometry column — not a spatial layer.")
        print(gdf.head(3))
