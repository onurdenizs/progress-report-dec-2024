import pandas as pd

# === CONFIGURATION ===
data_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\haltestellen_2025.csv"
sep = ","                  # <-- TAB-separated, not ;
encoding = "utf-8"       # Try 'latin1' or 'ISO-8859-1' if you hit encoding issues
chunksize = 100_000      # Adjust for memory
skiprows = 4             # <-- CHANGE this to skip garbage header lines if needed (try 4–10)

# === ANALYSIS FUNCTION ===
def process_chunk(df):
    print("\n--- CHUNK 1 ---")
    print("Sample rows:\n", df.head(3))
    
    print("\nColumns:", df.columns.tolist())
    print("\nColumn types:\n", df.dtypes.value_counts())

    datetime_cols = [col for col in df.columns if "datum" in col.lower() or "date" in col.lower()]
    if datetime_cols:
        print("\nLikely datetime columns:", datetime_cols)
    
    print("\nTop values from first object columns:\n")
    for col in df.select_dtypes(include="object").columns[:3]:
        print(f"{col}:\n{df[col].value_counts(dropna=False).head(3)}\n")

    print("-" * 60)

# === CHUNKED READING ===
try:
    for i, chunk in enumerate(pd.read_csv(
        data_file,
        sep=sep,
        encoding=encoding,
        engine="python",             # More tolerant
        quoting=3,                   # Ignore quotes
        on_bad_lines="skip",        # Skip bad lines
        skiprows=skiprows,          # Skip garbage headers
        chunksize=chunksize,
        quotechar='"',
        skipinitialspace=True
    )):
        process_chunk(chunk)
        break  # Only show first chunk
except Exception as e:
    print("❌ Error reading file:", e)
