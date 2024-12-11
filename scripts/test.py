import pandas as pd

# Load tripinfo data
tripinfo_df = pd.read_xml("D:/PhD/codingPractices/progress-report-dec-2024/outputs/sumo/tripinfo.xml")

# Analyze travel times
print(tripinfo_df[['id', 'depart', 'arrival', 'duration']])

# Visualize travel times
tripinfo_df['duration'].plot(kind='hist', bins=10, title='Distribution of Travel Times')
