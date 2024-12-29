import geopandas as gpd
import pandas as pd
import logging
from shapely.geometry import MultiLineString

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """Main function to process the input file and extract station information."""
    # Define input file path
    input_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\raw\swiss\linie_mit_polygon\linie_mit_polygon.geojson"
    output_file = r"D:\PhD\codingPractices\progress-report-dec-2024\data\processed\swiss\swiss_stations.csv"

    try:
        # Step 1: Read the input file with selected columns
        linie_df = gpd.read_file(input_file)[['km_agm_von', 'bp_anfang', 'bp_ende', 'linienr', 'geometry']]
        logging.info("Input file loaded successfully.")

        # Step 2: Create a list of unique bp_anfang and bp_ende values
        unique_bp_anfang = linie_df['bp_anfang'].unique()
        unique_bp_ende = linie_df['bp_ende'].unique()
        unique_station_list = list(set(unique_bp_anfang).union(set(unique_bp_ende)))
        logging.info(f"Unique station list created with {len(unique_station_list)} items.")

        # Step 3: Create an empty DataFrame for station information
        station_info = pd.DataFrame(columns=['station', 'coordinates'])

        # Step 4: Traverse through linie_df rows
        for _, row in linie_df.iterrows():
            # Process bp_anfang
            if row['bp_anfang'] not in station_info['station'].values:
                if isinstance(row['geometry'], MultiLineString):
                    first_coords = list(row['geometry'].geoms[0].coords)[0]
                else:
                    first_coords = list(row['geometry'].coords)[0]

                station_info = pd.concat([
                    station_info,
                    pd.DataFrame({'station': [row['bp_anfang']], 'coordinates': [first_coords]})
                ], ignore_index=True)

            # Process bp_ende
            if row['bp_ende'] not in station_info['station'].values:
                if isinstance(row['geometry'], MultiLineString):
                    last_coords = list(row['geometry'].geoms[-1].coords)[-1]
                else:
                    last_coords = list(row['geometry'].coords)[-1]

                station_info = pd.concat([
                    station_info,
                    pd.DataFrame({'station': [row['bp_ende']], 'coordinates': [last_coords]})
                ], ignore_index=True)

        # Step 5: Print the required information
        print(f"Number of unique stations in unique_station_list: {len(unique_station_list)}")
        print(f"Number of rows in station_info DataFrame: {len(station_info)}")

        # Step 6: Save station_info to a CSV file
        station_info.to_csv(output_file, index=False)
        logging.info(f"Station information saved to {output_file}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()