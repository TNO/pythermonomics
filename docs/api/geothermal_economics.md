# GeothermalEconomics

**Module:** `pythermonomics.geothermal_economics`

The `GeothermalEconomics` class is the main entry point for geothermal economics calculations. It combines configuration, simulation data, well trajectory, energy, and financial models to compute Net Present Value (NPV) and Levelized Cost of Energy (LCOE) for geothermal projects.

---

## Purpose

- Loads project settings and configuration from YAML files.
- Integrates simulation results (CSV format).
- Handles well trajectory and deviation files.
- Manages energy calculations, well cost modeling, and financial computations.
- Provides a unified API for running NPV/LCOE calculations.

---

## Main Attributes

- `economics_config`: Project configuration ([GeothermalEconomicsConfig](config/GeothermalEconomicsConfig.md))
- `simresults`: Well simulation results ([WellResults](data/WellResults.md) or [SimulationModelResults](data/SimulationModelResults.md))
- `welltrajectory`: Well trajectory object
- `wellcostmodel`: Well cost model ([CostModelWell](npv_model/CostModelWell.md))
- `energy_calculator`: Energy calculation model ([EnergyCalculator](energy_model/EnergyCalculator.md))
- `npv_calculator`: NPV calculation model ([EconomicsCalculator](npv_model/EconomicsCalculator.md))

---

## Main Methods

- `__init__(...)`: Initializes the class with configuration, simulation, and trajectory data.
- `compute_economics()`: Computes NPV, LCOE, cashflow, well results, and well states.
- `compute_energy(cashflow)`: Computes energy terms for the project.
- `from_trajectory(settingfile, trajectoryfile)`: Alternate constructor for well trajectory input.
- `from_config_only(settingfile)`: Alternate constructor for using only the config as input. 
- `from_summary_deviation_file(settingfile, summary_file, deviation_files_dir)`: Alternate constructor for simulation data and deviation files.
- `from_dc1d(settingfile, trajectoryfile, dc1dwell)`: Alternate constructor for DC1D well input.
---

## Usage

If you want to run the geothermal_economics based on a deviation file for each well and simulation data in 
csv format:
```python
from pythermonomics.geothermal_economics import GeothermalEconomics

economics = GeothermalEconomics.from_summary_deviation_file(
    settingfile='config_file.yml',
    summary_file='sim_data.csv',
    deviation_files_dir='dev_files/',
)

npv, lcoe_val, cashflow, wellRes, well_states, well_results = economics.compute_economics()
```

If you want to run the geothermal_economics based on only the config and a well trajectory file: 
```python
from pythermonomics.geothermal_economics import GeothermalEconomics

economics = GeothermalEconomics.from_trajectory(
    settingfile='config_file.yml',
    trajectoryfile='trajectoryfile,yml',
)

npv, lcoe_val, cashflow, wellRes, well_states, well_results = economics.compute_economics()
```

Running it just from the config is possible too: 
```python
from pythermonomics.geothermal_economics import GeothermalEconomics

economics = GeothermalEconomics.from_config_only(
    settingfile='config_file.yml',
)

npv, lcoe_val, cashflow, wellRes, well_states, well_results = economics.compute_economics()
```

Finally, it is also supported to run from a DC1DWell instance:
```python
from pythermonomics.geothermal_economics import GeothermalEconomics

class DummyDc1d:
    temp = [60, 120]
    salinity = [10000, 10000]
    rw = [0.1, 0.1]
    roughness = 0.05
    qvol = 0.05
    dpres = 30

dc1d = DummyDc1d()
economics = GeothermalEconomics.from_dc1d(
    settingfile='config_file.yml',
    dc1dwell=dc1d.
)

npv, lcoe_val, cashflow, wellRes, well_states, well_results = economics.compute_economics()
```

---

## CLI Entry Point

See [CLI Documentation](cli.md) for command-line usage.

---

## Related Components

- [GeothermalEconomicsConfig](config/GeothermalEconomicsConfig.md)
- [WellResults](data/WellResults.md)
- [SimulationModelResults](data/SimulationModelResults.md)
- [EnergyCalculator](energy_model/EnergyCalculator.md)
- [EconomicsCalculator](npv_model/EconomicsCalculator.md)
- [CostModelWell](npv_model/CostModelWell.md)