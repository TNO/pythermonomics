# PyThermoNomics

PyThermoNomics is a Python package for techno-economic analysis of geothermal energy projects. It provides tools to compute Net Present Value (NPV), Levelized Cost of Energy (LCOE), and related financial metrics using simulation data, well trajectories, and project configuration.

TODO: EXPAND HERE WHAT PROJECT IT WAS APART OF AND ADD LOGO ETC.

## Features

- Calculate NPV and LCOE for geothermal projects
- Integrate simulation results (CSV, OPM/Eclipse output)
- Model well trajectories and deviations
- Flexible configuration via YAML files
- Command-line interface (CLI) for easy usage
- Extensible API for custom workflows
- Documentation and tests included

## Installation

Install the package from the repository root:

```sh
pip install .
```

## Optional Dependencies

- **Documentation:**  
  To build and view the documentation, install with the `docs` extra:
  ```sh
  pip install .[docs]
  ```
- **Testing:**  
  To run tests, install with the `tests` extra:
  ```sh
  pip install .[tests]
  ```

## Usage

### Command-Line Interface

After installation, use the CLI tool:

```sh
geothermal-calc -c config.yml -i sim_data.csv -d deviations/ -t trajectory.yml
```

See [CLI Documentation](docs/api/cli.md) for all options.

### Python API

Import and use in your own scripts, for example, when using summary (reservoir simulation out in CSV format) and deviation files (XYZMD-records for each well):
```python
from pythermonomics.geothermal_economics import GeothermalEconomics

economics = GeothermalEconomics.from_summary_deviation_file(
    settingfile='config_file.yml',
    summary_file='sim_data.csv',
    deviation_files_dir='dev_files/',
)

npv, lcoe_val, cashflow, wellRes, well_states, well_results = economics.compute_economics()
```

or if you want to use `GeothermalEconomics` using only the config and a well trajectory file (see examples for a [trajectory file](tests/testdata/trajectory_files/inputsMultilateral3legs.yml)):
```python
from pythermonomics.geothermal_economics import GeothermalEconomics

economics = GeothermalEconomics.from_trajectory(
    settingfile='config_file.yml',
    trajectoryfile='trajectoryfile,yml',
)

npv, lcoe_val, cashflow, wellRes, well_states, well_results = economics.compute_economics()
```

## Documentation

Browse the full API reference and usage examples at [docs/index.md](docs/index.md) or build locally:

```sh
mkdocs serve
```

## Testing

Run the test suite with:

```sh
pytest
```

## Project Structure

```
src/
    pythermonomics/  # Main package code
        config/          
        data/
        energy_model/
        npv_model/
        cli.py
        geothermal_economics.py
docs/
    api/                   # API documentation
tests/                     # Unit and integration tests
pyproject.toml             # Package setup
mkdocs.yml                 # Documentation config
```

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

GNU General Public License v3 (GPLv3)

---

For more information, see the [API Reference](docs/index.md) or contact the maintainers.