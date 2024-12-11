"""
filter_selected_cities_lines.py

Script to filter lines where both origin and destination are among the selected cities,
with enhanced city name normalization.
"""

import pandas as pd
import os

# File paths
input_file = "D:/PhD/codingPractices/progress-report-dec-2024/data/processed/french/french_lines.csv"
output_dir = "D:/PhD/codingPractices/progress-report-dec-2024/data/processed/french"
output_file = os.path.join(output_dir, "selected_cities_lines.csv")

# Selected cities
selected_cities = ["Paris", "Strasbourg", "Nantes", "Rennes", "Dijon"]

try:
    print("Loading the french_lines.csv dataset...")
    # Load dataset
    df = pd.read_csv(input_file)
    print("Dataset loaded successfully!")

    print("Normalizing data for filtering...")
    # Normalize city names
    def normalize_city_name(city_name):
        if pd.isna(city_name):
            return ""
        # Remove descriptors in parentheses and convert to lowercase
        city_name = city_name.split("(")[0].strip().lower()
        # Normalize specific station variations
        replacements = {
            "paris-nord": "paris",
            "paris-gare-de-lyon": "paris",
            "paris-austerlitz": "paris",
            "strasbourg-ville": "strasbourg",
        }
        return replacements.get(city_name, city_name)

    df["origin"] = df["origin"].apply(normalize_city_name)
    df["destination"] = df["destination"].apply(normalize_city_name)

    # Prepare normalized selected cities for matching
    selected_cities_normalized = [city.lower() for city in selected_cities]

    print("Filtering lines based on selected cities...")
    # Filter rows where both origin and destination match selected cities
    filtered_lines = df[
        df["origin"].isin(selected_cities_normalized) &
        df["destination"].isin(selected_cities_normalized)
    ]

    print(f"{len(filtered_lines)} lines found between the selected cities.")

    print("Saving the filtered lines to a new file...")
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    filtered_lines.to_csv(output_file, index=False)
    print(f"Filtered data saved to: {output_file}")

except FileNotFoundError as fnfe:
    print(f"File not found: {fnfe}")
except KeyError as ke:
    print(f"Missing column: {ke}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
