import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt

# Paths
OUTPUT_DIR = r"D:/PhD/codingPractices/progress-report-dec-2024/outputs/french/"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "french_simulation_output.xml")

# Analysis Output
ANALYSIS_FILE = os.path.join(OUTPUT_DIR, "french_simulation_analysis.csv")


def parse_fcd_output(output_file):
    """
    Parses the FCD output file and extracts vehicle trajectory data.

    Args:
        output_file (str): Path to the FCD output XML file.

    Returns:
        DataFrame: A pandas DataFrame containing trajectory data.
    """
    tree = ET.parse(output_file)
    root = tree.getroot()

    # Initialize storage for trajectory data
    data = []

    for timestep in root.findall("timestep"):
        time = float(timestep.attrib["time"])
        for vehicle in timestep.findall("vehicle"):
            vehicle_id = vehicle.attrib["id"]
            x = float(vehicle.attrib["x"])
            y = float(vehicle.attrib["y"])
            speed = float(vehicle.attrib["speed"])
            data.append({"time": time, "vehicle_id": vehicle_id, "x": x, "y": y, "speed": speed})

    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df


def analyze_trajectories(df):
    """
    Performs basic analysis on vehicle trajectories.

    Args:
        df (DataFrame): DataFrame containing trajectory data.

    Returns:
        DataFrame: Summary statistics for each vehicle.
    """
    # Group by vehicle and calculate statistics
    summary = df.groupby("vehicle_id").agg(
        total_distance=("x", lambda x: x.diff().abs().sum()),
        avg_speed=("speed", "mean"),
        max_speed=("speed", "max"),
        total_time=("time", lambda t: t.max() - t.min()),
    ).reset_index()

    return summary


def plot_analysis(summary):
    """
    Generates graphs for the trajectory analysis.

    Args:
        summary (DataFrame): Summary statistics for each vehicle.

    Returns:
        None
    """
    # Plot total distance traveled by each vehicle
    plt.figure()
    summary.plot(x="vehicle_id", y="total_distance", kind="bar", legend=False)
    plt.title("Total Distance Traveled by Each Vehicle")
    plt.xlabel("Vehicle ID")
    plt.ylabel("Total Distance (meters)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "total_distance.png"))
    plt.show()

    # Plot average speed for each vehicle
    plt.figure()
    summary.plot(x="vehicle_id", y="avg_speed", kind="bar", color="orange", legend=False)
    plt.title("Average Speed of Each Vehicle")
    plt.xlabel("Vehicle ID")
    plt.ylabel("Average Speed (m/s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "average_speed.png"))
    plt.show()

    # Plot maximum speed for each vehicle
    plt.figure()
    summary.plot(x="vehicle_id", y="max_speed", kind="bar", color="green", legend=False)
    plt.title("Maximum Speed of Each Vehicle")
    plt.xlabel("Vehicle ID")
    plt.ylabel("Max Speed (m/s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "max_speed.png"))
    plt.show()


def main():
    # Parse the output file
    print("Parsing simulation output...")
    df = parse_fcd_output(OUTPUT_FILE)

    # Perform analysis
    print("Analyzing trajectories...")
    summary = analyze_trajectories(df)

    # Print summary to the console
    print("\n=== Simulation Analysis Summary ===")
    print(summary)

    # Save analysis to CSV
    summary.to_csv(ANALYSIS_FILE, index=False)
    print(f"\nAnalysis saved to: {ANALYSIS_FILE}")

    # Generate graphs
    print("\nGenerating graphs...")
    plot_analysis(summary)


if __name__ == "__main__":
    main()
