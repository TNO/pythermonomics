# EconomicsCalculator

**Module:** `pythermonomics.npv_model.economics_calculator`

Main class for NPV and LCOE calculations.

## Purpose

- Computes Net Present Value (NPV) and Levelized Cost of Energy (LCOE) for geothermal projects.
- Integrates energy calculations, CAPEX/OPEX, and financial metrics.

## Main Methods

- `compute_economics()`: Returns NPV, LCOE, cashflow DataFrame, well results, and well states.

## Usage

```python
from pythermonomics.npv_model.economics_calculator import EconomicsCalculator

calc = EconomicsCalculator(economics_instance=economics_instance)
npv, lcoe, cashflow, wellRes, well_states = calc.compute_economics()
```