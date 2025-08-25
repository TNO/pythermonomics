# YAML Configuration Specification

This page describes the structure and meaning of the YAML configuration file (`input.yaml`) used for geothermal economics calculations. Each section of the YAML file corresponds to a Pydantic config class in the codebase, providing validation and documentation for all parameters.

---

## Top-Level Structure

A typical configuration file looks like:

```yaml
energy_loss_parameters:
  well_roughness: 0.138
  well_tubing: 8.5
  useheatloss: true
  tsurface: 10.0
  tgrad: 0.031

reservoir_simulation_parameters:
  injection_temperature: 50
  production_temperature: 90
  injection_BHP: 260
  production_BHP: 200
  flowrate: 400
  salinity: 140000

techno_economic_parameters:
  loadhours: 6000
  wellcost_scaling: 1.5
  wellcost_base: 250000
  well_curvfac: 1.0
  wellcost_linear: 700
  wellcost_cube: 0.2
  pump_efficiency: 0.6
  pump_cost: 500000
  pump_life: 5
  CAPEX_base: 3000000
  CAPEX_variable: 300
  CAPEX_contingency: 0.15
  OPEX_base: 0
  OPEX_variable: 100
  OPEX_variable_produced: 0.19
  equity_share: 0.2
  loan_nyear: 15
  loan_rate: 0.05
  discount_rate: 0.145
  inflation_rate: 0.015
  tax_rate: 0.25
  tax_depreciation_nyear: 15
  heat_price: 5.1
  heat_price_feedin: 5.1
  electricity_price: 8
  lifecycle_years: 15
  subsidy_years: 15

well_trajectories:
  INJ1:
    platform: [0, 0, 0.0]
    kick_off: [0, 0, 800.0]
    targets: [[800, 500, 2300], [1800, 500, 2400]]
  PRD1:
    platform: [0, 0, 0.0]
    kick_off: [0, 0, 800.0]
    targets: [[800, -500, 2300], [1800, -500, 2400]]
```

---

## Sections and Their Classes

### 1. `energy_loss_parameters`
**Class:** [`EnergyLossParameters`](../api/config/EnergyLossParameters.md)

- `well_roughness`: Well roughness in milli-inch.
- `well_tubing`: Production tubing diameter in inches.
- `useheatloss`: (Optional) Enable/disable heat loss calculations.
- `tsurface`: (Optional) Surface temperature in °C.
- `tgrad`: (Optional) Geothermal gradient in °C/m.

See: [`EnergyLossParameters`](../api/config/EnergyLossParameters.md)

---

### 2. `reservoir_simulation_parameters`
**Class:** [`ReservoirSimulationParameters`](../api/config/ReservoirSimulationParameters.md)

This simulation class will be used if you don't prescribe any simulation time series, see [SimulationTimeSeries](SimulationTimeSeries.md)

- `injection_temperature`: Injection temperature (°C).
- `production_temperature`: Production temperature (°C).
- `injection_BHP`: Injection bottom-hole pressure (bar).
- `production_BHP`: Production bottom-hole pressure (bar).
- `flowrate`: Flowrate (m³/h).
- `salinity`: Brine salinity (ppm).

See: [`ReservoirSimulationParameters`](../api/config/ReservoirSimulationParameters.md)

---

### 3. `techno_economic_parameters`
**Class:** [`TechnoEconomicParameters`](../api/config/TechnoEconomicParameters.md)

Contains all economic and technical parameters for the project, such as:

- `loadhours`: Operational hours per year.
- `wellcost_scaling`, `wellcost_base`, `well_curvfac`, `wellcost_linear`, `wellcost_cube`: Well cost model parameters.
- `pump_efficiency`, `pump_cost`, `pump_life`: Pump parameters.
- `CAPEX_base`, `CAPEX_variable`, `CAPEX_contingency`: Capital expenditure parameters.
- `OPEX_base`, `OPEX_variable`, `OPEX_variable_produced`: Operational expenditure parameters.
- `equity_share`, `loan_nyear`, `loan_rate`, `discount_rate`, `inflation_rate`: Financial parameters.
- `tax_rate`, `tax_depreciation_nyear`: Taxation parameters.
- `heat_price`, `heat_price_feedin`, `electricity_price`: Energy price parameters.
- `nyear`, `subsidy_years`: Project duration and subsidy.

See: [`TechnoEconomicParameters`](../api/config/TechnoEconomicParameters.md)

---

### 4. `well_trajectories`
**Class:** [`WellTrajectory`](../api/config/WellTrajectory.md)

A dictionary mapping well names to their spatial configuration:

- `platform`: `[x, y, z]` coordinates of the well platform.
- `kick_off`: `[x, y, z]` coordinates of the well kick-off point.
- `targets`: List of `[x, y, z]` reservoir target coordinates.

See: [`WellTrajectory`](../api/config/WellTrajectory.md)

---

## Loading and Validation

The YAML file is loaded and validated using the [`GeothermalEconomicsConfig`](../api/config/GeothermalEconomicsConfig.md) class, which ensures all required fields are present and correctly typed.

```python
from pythermonomics.config.geothermal_economics_config import GeothermalEconomicsConfig

config = GeothermalEconomicsConfig.load_from_file("input.yaml")
```

---

## Further Reading

- [API Reference: Config Classes](../api/config.md)
