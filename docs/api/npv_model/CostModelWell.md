# CostModelWell

**Module:** `pythermonomics.npv_model.costmodel_well`

Computes costs for wells based on well trajectories.

## Purpose

- Calculates well costs for multilateral and standard wells.
- Integrates with well trajectory and project parameters.

## Main Methods

- `compute_costs()`: Returns total well costs.

## Usage

```python
from pythermonomics.npv_model.costmodel_well import CostModelWell

cost_model = CostModelWell(geothermal_economics_instance=geothermal_economics_instance)
costs = cost_model.compute_costs()
```