# GeothermalEconomicsConfig

**Module:** `pythermonomics.config.geothermal_economics_config`

Loads and validates configuration for geothermal economics calculations.

## Purpose
- Loads configuration from YAML files.
- Validates and provides access to project parameters, well definitions, and reservoir settings.
- Supports optional configuration of reservoir simulation and energy loss parameters.

## Related Classes

- [TechnoEconomicParameters](TechnoEconomicParameters.md)
- [ReservoirSimulationParameters](ReservoirSimulationParameters.md)
- [EnergyLossParameters](EnergyLossParameters.md)
- [WellTrajectory](WellTrajectory.md)

## Main Methods

- `load_from_file(path)`: Loads configuration from a YAML file.
- `validate()`: Validates the loaded configuration data.

## Usage

```python
from pythermonomics.config.geothermal_economics_config import GeothermalEconomicsConfig

config = GeothermalEconomicsConfig.load_from_file(path="config.yml")

parameters = config.techno_eco_param
sim_params = config.reservoir_parameters
energy_loss_params = config.energy_loss_parameters
well_trajectories = config.well_trajectories

```