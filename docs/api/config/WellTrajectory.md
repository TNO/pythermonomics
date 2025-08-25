# WellTrajectory

**Module:** `pythermonomics.config.well_trajectories_config`

Configuration for well trajectories in geothermal economics.

## Purpose

- Defines the spatial configuration of a single well, including platform location, kick-off point, and reservoir targets.
- Used to model well paths for simulation and cost calculations.

## Main Fields

- `platform`: List of three floats `[x, y, z]` — Coordinates of the platform.
- `kick_off`: List of three floats `[x, y, z]` — Kick-off point of the well.
- `targets`: List of lists of three floats `[[x, y, z], ...]` — Target coordinates, e.g., top and bottom of the reservoir.

## Example YAML

```yaml
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

In this structure, each well name (e.g., `INJ1`, `PRD1`) maps to a `WellTrajectory` configuration.

## Usage

```python
from pythermonomics.config.well_trajectories_config import WellTrajectory

well_trajectories = {
    "INJ1": WellTrajectory(
        platform=[0, 0, 0.0],
        kick_off=[0, 0, 800.0],
        targets=[[800, 500, 2300], [1800, 500, 2400]],
    ),
    "PRD1": WellTrajectory(
        platform=[0, 0, 0.0],
        kick_off=[0, 0, 800.0],
        targets=[[800, -500, 2300], [1800, -500, 2400]],
    ),
}
```
