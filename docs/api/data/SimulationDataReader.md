# SimulationDataReader

**Module:** `pythermonomics.data.read_sim_data_from_csv`

Reads OPM/Eclipse simulation data from CSV files.

## Purpose

- Extracts well names and states from simulation output.
- Provides access to relevant time-series results for further calculations.

## Main Methods

- `get_relevant_simulation_results()`: Returns a DataFrame with required simulation results.
- `extract_well_names_from_csv()`: Extracts well names from CSV columns.
- `extract_well_states_final_timestep()`: Gets well states at the final timestep.
- `add_single_temperature_column()`: Adds a temperature column to the DataFrame.

## Usage

```python
from pythermonomics.data.read_sim_data_from_csv import SimulationDataReader

reader = SimulationDataReader(csv_file="simulation.csv")
results = reader.get_relevant_simulation_results()
```