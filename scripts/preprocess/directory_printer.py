import os
import pandas as pd

# Define known delimiters for problematic files
KNOWN_DELIMITERS = {
    "didok.csv": ";",
    "ist_daten_sbb.csv": ";",
}

def analyze_directory_csv(base_path):
    """
    Analyzes CSV files in subdirectories of the given base path with enhanced error handling and specific delimiters.

    Args:
        base_path (str): The base directory containing subdirectories to analyze.
    """
    directories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
    
    for directory in directories:
        dir_path = os.path.join(base_path, directory)
        print(f"\nAnalyzing directory: {directory}")
        print("-" * 50)
        
        csv_file_name = f"{directory}.csv"
        csv_file_path = os.path.join(dir_path, csv_file_name)
        
        if not os.path.exists(csv_file_path):
            print(f"No CSV file named '{csv_file_name}' found in '{directory}'.")
            continue
        
        print(f"\nFound matching file: {csv_file_name}")
        print("-" * 30)
        
        try:
            # Use known delimiter if available
            delimiter = KNOWN_DELIMITERS.get(csv_file_name, None)
            if not delimiter:
                # Attempt automatic delimiter detection
                with open(csv_file_path, 'r', encoding='utf-8') as file:
                    sample = file.read(2048)
                    delimiter = csv.Sniffer().sniff(sample).delimiter
                print(f"Detected delimiter: '{delimiter}'")
            
            # Read the CSV file
            df = pd.read_csv(csv_file_path, delimiter=delimiter, on_bad_lines='skip', low_memory=False)
            
            # Display dataset details
            print(f"Columns: {list(df.columns)}")
            print("\nFirst 5 rows:")
            print(df.head())
            print("\nDataFrame Info:")
            df.info()
            
            # Summary statistics
            if not df.empty:
                print("\nSummary Statistics:")
                print(df.describe(include='all'))
        except Exception as e:
            print(f"Error processing '{csv_file_name}': {e}")
        print("\n" + "=" * 50)

# Define the base path
base_path = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss"

# Run the analysis
analyze_directory_csv(base_path)
