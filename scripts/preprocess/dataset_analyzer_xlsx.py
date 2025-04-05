import pandas as pd

data_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\t01x-sbb-cff-ffs-frequentia-2023.xlsx"

# 1. List all sheet names
xls = pd.ExcelFile(data_file)
print("📄 Sheets in this Excel file:")
for sheet in xls.sheet_names:
    print(f"  - {sheet}")

# 2. Load each sheet one by one and show top rows
for sheet in xls.sheet_names:
    print(f"\n--- Analyzing sheet: {sheet} ---")
    try:
        df = pd.read_excel(data_file, sheet_name=sheet)
        print(df.head(3))
        print(f"\n✅ Columns: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Failed to load {sheet}: {e}")
