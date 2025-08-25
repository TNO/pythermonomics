# SimulationModelResults

**Module:** `pythermonomics.data.simulation_model_results`

Reads simulation results from summary file (CSV) and well-paths from deviation files.

## Purpose

- Combines summary simulation results and deviation file data for wells.
- Provides a unified interface for downstream calculations.

## Main Methods

- `__init__()`: Loads summary and deviation data for wells.

## Usage

```python
from pythermonomics.data.simulation_model_results import SimulationModelResults

results = SimulationModelResults(
    summary_file="summary.csv",
    path_deviation_files="deviation_dir/",
)
```