import pandas as pd
import matplotlib.pyplot as plt

# Read the tripinfo.xml
tripinfo_df = pd.read_xml("D:/PhD/codingPractices/progress-report-dec-2024/outputs/sumo/tripinfo.xml")

# Basic Metrics
tripinfo_df["average_speed"] = tripinfo_df["routeLength"] / tripinfo_df["duration"]

# Duration Comparison
plt.bar(tripinfo_df["id"], tripinfo_df["duration"], color='skyblue')
plt.title("Trip Duration per Train")
plt.xlabel("Train ID")
plt.ylabel("Duration (seconds)")
plt.show()

# Average Speed vs Route Length
plt.scatter(tripinfo_df["routeLength"], tripinfo_df["average_speed"], color='green')
plt.title("Average Speed vs Route Length")
plt.xlabel("Route Length (meters)")
plt.ylabel("Average Speed (m/s)")
plt.show()

# Gantt Chart for Train Timelines
for _, row in tripinfo_df.iterrows():
    plt.hlines(row["id"], row["depart"], row["arrival"], colors='blue', lw=4)
plt.title("Train Schedules")
plt.xlabel("Time (seconds)")
plt.ylabel("Train ID")
plt.show()
