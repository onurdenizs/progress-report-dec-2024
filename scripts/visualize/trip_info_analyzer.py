import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# Path to tripinfo-output file
TRIPINFO_FILE = "D:\\PhD\\codingPractices\\progress-report-dec-2024\\sumo\\outputs\\sw_real_comp\\sw_comp_output.tripinfo.xml"


def parse_tripinfo(file_path):
    """
    Parse the tripinfo XML file and return a DataFrame with key metrics.

    Args:
        file_path (str): Path to the tripinfo XML file.

    Returns:
        pd.DataFrame: A DataFrame containing parsed tripinfo data.
    """
    data = []
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        for trip in root.findall("tripinfo"):
            data.append({
                "train_id": trip.get("id"),
                "depart": float(trip.get("depart")),
                "arrival": float(trip.get("arrival")),
                "duration": float(trip.get("duration")),
                "route_length": float(trip.get("routeLength")),
                "stop_time": float(trip.get("stopTime")),
                "CO2_abs": float(trip.find("emissions").get("CO2_abs")),
                "fuel_abs": float(trip.find("emissions").get("fuel_abs")),
            })
    except Exception as e:
        print(f"Error parsing tripinfo file: {e}")
        return None
    
    return pd.DataFrame(data)

def plot_duration_vs_emissions(df):
    """
    Plot Train Duration vs. CO2 Emissions.

    Args:
        df (pd.DataFrame): DataFrame containing tripinfo data.
    """
    plt.figure(figsize=(10, 6))
    plt.scatter(df["duration"], df["CO2_abs"], alpha=0.7)
    plt.title("Train Duration vs. CO2 Emissions")
    plt.xlabel("Duration (seconds)")
    plt.ylabel("CO2 Emissions (g)")
    plt.grid()
    plt.show()

def plot_stop_times(df):
    """
    Plot Stop Times for Different Trains.

    Args:
        df (pd.DataFrame): DataFrame containing tripinfo data.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(df["train_id"], df["stop_time"])
    plt.title("Stop Times for Different Trains")
    plt.xlabel("Train ID")
    plt.ylabel("Total Stop Time (seconds)")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

def plot_fuel_consumption(df):
    """
    Plot Fuel Consumption Across Trains.

    Args:
        df (pd.DataFrame): DataFrame containing tripinfo data.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(df["train_id"], df["fuel_abs"], color='orange')
    plt.title("Fuel Consumption Across Trains")
    plt.xlabel("Train ID")
    plt.ylabel("Fuel Consumption (ml)")
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.show()

def main():
    """
    Main function to parse tripinfo data and generate visualizations.
    """
    print("Parsing tripinfo file...")
    tripinfo_df = parse_tripinfo(TRIPINFO_FILE)
    
    if tripinfo_df is not None:
        print("Data parsed successfully. Generating visualizations...")
        print("Summary of parsed data:")
        print(tripinfo_df.describe())
        
        plot_duration_vs_emissions(tripinfo_df)
        plot_stop_times(tripinfo_df)
        plot_fuel_consumption(tripinfo_df)
    else:
        print("Failed to parse tripinfo file.")

if __name__ == "__main__":
    main()
