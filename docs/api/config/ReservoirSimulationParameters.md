# ReservoirSimulationParameters

**Module:** `pythermonomics.config.reservoir_simulation_parameters`

Reservoir-specific configuration for simulation and economics.

## Purpose

- Stores reservoir-specific settings such as production temperature, BHP, and flowrate.
- Used for simulation and economics calculations.

## Main Fields

- `injection_temperature`: Injection temperature (°C)
- `production_temperature`: Production temperature (°C)
- `injection_BHP`: Injection bottom hole pressure (bar)
- `production_BHP`: Production bottom hole pressure (bar)
- `flowrate`: Flowrate (m³/h)
- `salinity`: Salinity used for brine heat capacity (ppm)

## Usage

```python
from pythermonomics.config.reservoir_simulation_parameters import ReservoirSimulationParameters

res_params = ReservoirSimulationParameters(
    production_temperature=90,
    injection_BHP=260,
    # ...other parameters...
)
```