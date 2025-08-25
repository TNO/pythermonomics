# WellResults

**Module:** `pythermonomics.data.well_results`

Reads simulated well paths and production characteristics over time from provided configuration data.

## Purpose

- Manages well path and production data.
- Provides access to time-series results and well states for further calculations.

## Main Methods

- `read_wellpaths_production()`: Reads well paths and production characteristics.
- `read_well_path_and_types()`: Reads well path and types.

## Usage

```python
from pythermonomics.data.well_results import WellResults

well_results = WellResults(
    wells=wells,
    reservoir_parameters=reservoir_parameters,
    parameters=parameters,
    nyear=nyear,
)
df, states, coords = well_results.read_wellpaths_production()
```