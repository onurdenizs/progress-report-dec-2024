# Swiss Railway Network Simulation Project

This project aims to simulate the Swiss railway network in SUMO with basic Virtual Coupling concepts. It includes tools and scripts to process railway datasets, generate SUMO-compatible network files, and run simulations. This project is intended to be accessible to both developers and non-coding users.

## Getting Started

### For Developers

#### Clone the Repository

```bash
git clone https://github.com/your-username/progress-report-dec-2024.git
cd progress-report-dec-2024

conda env create -f environment.yml
conda activate swiss-network-sumo

pip install -r requirements.txt
```

Explore and run scripts in the scripts/ folder to customize or extend the project.

### For Non-Coding Users

1. **Install SUMO**: Follow the official [SUMO Installation Guide](https://sumo.dlr.de/docs/Downloads.php).
2. **Download this Project**:
   - [Download as ZIP](https://github.com/your-username/progress-report-dec-2024/archive/refs/heads/main.zip)
3. **Extract**: Extract the project to a folder of your choice.
4. **Navigate**: Go to the `sumo/inputs/` folder.
5. **Follow the Guide**: Refer to the **User Guide** in the `docs/` folder for detailed instructions.

### How to Use

#### Running the Simulation

1. Ensure **SUMO** is installed and the project is set up.
2. Navigate to the `sumo/inputs/` folder.
3. Run the following command to start the simulation:
   ```bash
   sumo-gui -c swiss_network.sumocfg
   ```

#### Customizing the Network

Use the scripts/ folder to process new datasets or customize the network.
Modify the sumo/inputs/swiss_network.net.xml file for advanced edits.

### Documentation

- **For Developers**: Refer to `docs/developer_guide.md` for detailed instructions on extending the project.
- **For Non-Coding Users**: Refer to `docs/user_guide.md` for step-by-step instructions and troubleshooting tips.

### Contributing

We welcome contributions! Please read the `CONTRIBUTING.md` file for guidelines on how to contribute to this project.

### License

This project is licensed under the MIT License. See the `LICENSE` file for details.

### Contact

For questions or support, open an issue on GitHub or reach out at:

- **Email**: onurdnz@gmail.com
- **GitHub**: [onurdenizs](https://github.com/onurdenizs)
