# pythermonomics.config API Reference

This module provides configuration models and utilities for geothermal economics calculations.

## Classes

- [`GeothermalEconomicsConfig`](config/GeothermalEconomicsConfig.md): Loads and validates configuration for NPV and LCOE calculations, including project parameters, well definitions, and reservoir settings.
- [`TechnoEconomicParameters`](config/TechnoEconomicParameters.md): Defines techno-economic parameters required for NPV and LCOE calculations.
- [`ReservoirSimulationParameters`](config/ReservoirSimulationParameters.md): Reservoir-specific configuration for simulation.
- [`EnergyLossParameters`](config/EnergyLossParameters.md): Energy loss related parameters.
- [`WellTrajectory`](config/WellTrajectory.md): Very basic definition of well trajectory.

---

## API Details

- [GeothermalEconomicsConfig](config/GeothermalEconomicsConfig.md):  
  Handles loading from YAML files, validation of configuration data, and provides access to all project parameters required for economics and simulation.

- [TechnoEconomicParameters](config/TechnoEconomicParameters.md):  
  Contains all the techno-economic geothermal system parameters (loadhours, pumpcosts, etc.) used in calculations.

- [ReservoirSimulationParameters](config/ReservoirSimulationParameters.md):  
  Contains reservoir-specific settings such as production temperature, BHP, and flowrate.

- [EnergyLossParameters](config/EnergyLossParameters.md):  
  Contains energy loss related parameters such as well roughness and tubing size.

- [WellTrajectory](config/WellTrajectory.md):  
  Contains very basic description of a well trajectory

---

## Class Documentation

- [GeothermalEconomicsConfig](config/GeothermalEconomicsConfig.md)
- [TechnoEconomicParameters](config/TechnoEconomicParameters.md)
- [ReservoirSimulationParameters](config/ReservoirSimulationParameters.md)
- [EnergyLossParameters](config/EnergyLossParameters.md)
- [WellTrajectory](config/WellTrajectory.md)