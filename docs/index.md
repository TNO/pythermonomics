<p align="center">
  <img src="logo/logo_PyThermoNomics.png" alt="PyThermoNomics Logo" width="300"/>
</p>

# PyThermoNomics

Welcome to the PyThermoNomics documentation!

This project provides tools for geothermal economics calculations, including Net Present Value (NPV) and Levelized Cost of Energy (LCOE) computations, well simulation, and more.

## Modules

- [geothermal_economics](api/geothermal_economics.md): Main API for economics calculations.
- [config](api/config.md): Configuration models and utilities.
- [energy_model](api/energy_model.md): Energy calculation models.
- [data](api/data.md): Simulation readers and well results.
- [npv_model](api/npv_model.md): NPV and cost models.

## API Reference

Explore the API documentation for each module:

- [geothermal_economics](api/geothermal_economics.md)
- [config](api/config.md)
- [energy_model](api/energy_model.md)
- [data](api/data.md)
- [npv_model](api/npv_model.md)

## Getting Started

To get started, see the [README](https://github.com/TNO/pythermonomics) or browse the API reference above.

## Examples

An example of how to run a case for a doublet system for a real reservoir model is shown in the Jupyter Notebook found in `examples/main_example_notebook.ipynb`. 
Explanation on how to install Jupyter Notebook can be found [here](examples/UseJupyTerNotebook.md).

## Input description

- [InputConfigYaml](input_description/InputConfigYaml.md)
- [InputDeviationFiles](input_description/InputDeviationFiles.md)
- [SimulationTimeSeries](input_description/SimulationTimeSeries.md)

## Column description of output DataFrame/CSV

- [ColumnNames](output_description/CashflowColumnNames.md)

## Net Present Value equations

To see the equations related to the NPV and LCOE please see [Equations](equations/NpvAndLcoeEquations.md).

## Development notes

Notes on the development including assumptions and limitations are mentioned in [DevelopmentNotes](development_notes/LimitationsAndAssumptions.md).
