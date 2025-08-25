# EnergyCalculator

**Module:** `pythermonomics.energy_model.energy_calculator`

Main class for geothermal energy calculations.

## Purpose

- Computes energy production, injection, and temperature profiles for geothermal wells.
- Integrates simulation results and well trajectory data.

## Main Methods

- `compute_energy(cashflow)`: Calculates energy terms and updates the cashflow DataFrame.

## Usage

```python
from pythermonomics.energy_model.energy_calculator import EnergyCalculator

calc = EnergyCalculator(economics_instance=economics_instance)
cashflow, nwp, nwi = calc.compute_energy(cashflow=cashflow)
```