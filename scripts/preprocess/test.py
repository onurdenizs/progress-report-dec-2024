import geopandas as gpd

# Path to your GPKG file
data_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\swissTNE_Base_20240507.gpkg"

# Load the edge geometries and base type lookup table
gdf_edges = gpd.read_file(data_file, layer="bn_edge")
df_basetype = gpd.read_file(data_file, layer="lut_base_type")

# 🔍 Inspect column types to debug mapping issues
print("➡️ gdf_edges['basetype'] dtype:", gdf_edges["basetype"].dtype)
print("➡️ df_basetype['object_key'] dtype:", df_basetype["object_key"].dtype)

# 🧼 Ensure the key columns are of the same type (string)
gdf_edges["basetype"] = gdf_edges["basetype"].astype(str)
df_basetype["object_key"] = df_basetype["object_key"].astype(str)

# 🗺️ Create mapping from basetype code to short label
mapping = dict(zip(df_basetype["object_key"], df_basetype["value_short_en"]))

# 🏷️ Add a new column to edges with readable base type
gdf_edges["basetype_label"] = gdf_edges["basetype"].map(mapping)

# 📊 Print counts of each base type label
print("🔎 Mapped base types (with readable labels):")
print(gdf_edges["basetype_label"].value_counts())
