# pythermonomics.data API Reference

This module provides classes for reading, processing, and managing simulation data, well results, and deviation files for geothermal projects.

## Classes

- [`SimulationDataReader`](data/SimulationDataReader.md): Reads OPM/Eclipse simulation data from CSV files, extracts well names, states, and relevant time-series data.
- [`DeviationFileReader`](data/DeviationFileReader.md): Reads deviation files for wells and extracts well name and coordinates.
- [`WellResults`](data/WellResults.md): Reads simulated well paths and production characteristics over time from provided configuration data.
- [`SimulationModelResults`](data/SimulationModelResults.md): Reads simulation results from summary files and well-paths from deviation files.

---

## API Details

- [SimulationDataReader](data/SimulationDataReader.md):  
  Handles extraction of well names, states, and time-series results from simulation CSV files.  
  Useful for integrating OPM/Eclipse output into the economics workflow.

- [DeviationFileReader](data/DeviationFileReader.md):  
  Parses well deviation files to obtain well trajectory and coordinate data.  
  Ensures correct mapping of well names to their spatial data.

- [WellResults](data/WellResults.md):  
  Manages well path and production data, providing access to time-series results and well states.  
  Used for further energy and financial calculations.

- [SimulationModelResults](data/SimulationModelResults.md):  
  Combines summary simulation results and deviation file data for wells.  
  Provides a unified interface for downstream calculations.

---

## Class Documentation

- [SimulationDataReader](data/SimulationDataReader.md)
- [DeviationFileReader](data/DeviationFileReader.md)
- [WellResults](data/WellResults.md)
- [SimulationModelResults](data/SimulationModelResults.md)