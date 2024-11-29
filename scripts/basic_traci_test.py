import os
import sys
import traci

# Set SUMO_HOME if not set
if 'SUMO_HOME' not in os.environ:
    os.environ['SUMO_HOME'] = 'C:/Program Files (x86)/Eclipse/Sumo'
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))

# Define SUMO binary and configuration file
sumo_binary = os.path.join(os.environ['SUMO_HOME'], 'bin', 'sumo-gui')
sumo_config = "data/simple_sumo_example/simple_config.sumocfg"  # Update this with your config file

# Define SUMO command
sumoCmd = [
    "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui",
    "-c", "C:/Users/onurd/OneDrive/Masaüstü/PhD/codingPractices/progress-report-dec-2024/data/simple_sumo_example/simple_config.sumocfg",
    "--log", "logs/sumo.log"
]


print(f"Starting SUMO with command: {' '.join(sumoCmd)}")

try:
    # Start SUMO
    traci.start(sumoCmd)
    print("SUMO started successfully.")

    # Simulation loop
    for step in range(10):
        traci.simulationStep()
        print(f"Step {step} completed.")

    traci.close()
except Exception as e:
    print(f"An error occurred: {e}")
