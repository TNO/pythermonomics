# Simulation Data (CSV) Specification

This page describes the format and usage of simulation data input files, which are used to provide time-series results for all wells in a geothermal project.

---

## File Format

A simulation data file is a CSV file with the following structure:

- The first row contains column headers (keywords).
- Each subsequent row contains time-series data for a single timestep.
- Columns include both global and well-specific keywords.

**Example (header and first data row):**

```csv
,DATES,YEARS,FPR,WBHP:INJ1,WBHP:PRD1,WSTAT:INJ1,WSTAT:PRD1,WTICHEA:INJ1,WTICHEA:PRD1,WTPCHEA:INJ1,WTPCHEA:PRD1,WWIR:INJ1,WWIR:PRD1,WWPR:INJ1,WWPR:PRD1,WWIT:INJ1,WWIT:PRD1,WWPT:INJ1,WWPT:PRD1,DAYS
0,2020-01-01 00:00:00,0.08,257.97,0.0,0.0,3.0,3.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,30.99
```

---

## Column Definitions

### Global Columns (appear once)

- **DATES**: Date/time of the simulation step (string or datetime)
- **YEARS**: Simulation time in years (float)
- **FPR**: Field pressure (float)
- **DAYS**: Simulation time in days (float, may be computed from YEARS)

### Well-Related Columns (repeat for each well)

These columns are named as `KEYWORD:WELLNAME` (e.g., `WBHP:INJ1`, `WSTAT:PRD1`):

- **WBHP:** Bottom-hole pressure (bar)
- **WSTAT:** Well state (1.0 = production, 2.0 = injection, 3.0 = shut-in)
- **WTICHEA:** Injection well temperature (°C)
- **WTPCHEA:** Production well temperature (°C)
- **WWIR:** Water injection rate (m³/d)
- **WWIT:** Water injection total (m³)
- **WWPR:** Water production rate (m³/d)
- **WWPT:** Water production total (m³)
- *(Other well-related keywords may be present depending on the simulator and configuration)*

**Note:**  
Each well will have its own set of columns for each well-related keyword.

---

## Example (abbreviated)

```csv
,DATES,YEARS,FPR,WBHP:INJ1,WBHP:PRD1,WSTAT:INJ1,WSTAT:PRD1,WTICHEA:INJ1,WTICHEA:PRD1,WTPCHEA:INJ1,WTPCHEA:PRD1,WWIR:INJ1,WWIR:PRD1,WWPR:INJ1,WWPR:PRD1,WWIT:INJ1,WWIT:PRD1,WWPT:INJ1,WWPT:PRD1,DAYS
0,2020-01-01 00:00:00,0.08,257.97,0.0,0.0,3.0,3.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,30.99
1,2021-01-01 00:00:00,1.08,257.96,256.38,2.0,1.0,30.0,0.0,0.0,80.0,99.63,0.0,8000.0,0.0,8000.0,0.0,8000.0,397.00
...
```

---

## Usage in the Code

Simulation data files are read using the [`SimulationDataReader`](../api/data/SimulationDataReader.md) class:

```python
from pythermonomics.data.read_sim_data_from_csv import SimulationDataReader

reader = SimulationDataReader(csv_file="simulation_time_series.csv")
results = reader.get_relevant_simulation_results()
```

- The reader will automatically extract well names, states, and relevant time-series data for each well.

---

## Notes

- The file must contain all required global and well-related columns as expected by the code.
- Well-related columns must use the `KEYWORD:WELLNAME` format.
- The code will validate the presence of all required columns and raise an error if any are missing.
- The `DAYS` column may be computed if not present, based on `YEARS`.

---

## Example Directory Structure

```
summary_files/
  simulation_time_series.csv
  ...
```

And you simply refer to the file path in your arguments when running either the [CLI](../api/cli.md) or use it directly in your [python code](../api/geothermal_economics.md):

---

For more details, see the [SimulationDataReader API documentation](../api/data/SimulationDataReader.md).