# EnergyLossParameters

**Module:** `pythermonomics.config.energy_loss_parameters`

Parameters related to energy losses from well to the surface.

## Purpose

- Stores settings such as well_roughness and well_tubing.
- Used for calculating energy losses in the energy calculations.

## Main Fields

- `well_roughness`: Roughness of the well (milli inch)
- `well_tubing`: Production tubing (inch)
- `useheatloss`: Use calculated heatlosses in energy calculation (-)
- `tsurface`: Surface temerpature (°C)
- `tgrad`: Temperature gradient in subsurface (°C/m)

## Usage

```python
from pythermonomics.config.energy_loss_parameters import EnergyLossParameters

energy_loss_params = EnergyLossParameters(
    well_roughness=0.138,
    well_tubing=8.5,
    # ...other parameters...
)
```