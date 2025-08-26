<p align="center">
  <img src="docs/logo/logo_PyThermoNomics.png" alt="PyThermoNomics Logo" width="300"/>
</p>

# PyThermoNomics

PyThermoNomics is a Python package for techno-economic analysis of geothermal energy projects. It provides tools to compute Net Present Value (NPV), Levelized Cost of Energy (LCOE), and related financial metrics using simulation data, well trajectories, and project configuration.

## Features

- Calculate NPV and LCOE for geothermal projects
- Integrate simulation results (CSV, OPM/Eclipse output)
- Model well trajectories and deviations
- Flexible configuration via YAML files
- Command-line interface (CLI) for easy usage
- Extensible API for custom workflows
- Documentation and tests included

### Reference in the literature

The PyThermoNomics has been used in:
 
Barros, E.G.D.; Szklarz, S.P.; Khoshnevis Gargar, N.; Wollenweber, J.; van Wees, J.D. Optimization of Well Locations and Trajectories: Comparing Sub-Vertical, Sub-Horizontal and Multi-Lateral Well Concepts for Marginal Geothermal Reservoir in The Netherlands. Energies 2025, 18, 627. [DOI](https://doi.org/10.3390/en18030627)

## Installation

Install the latest version using pip:

```sh
pip install pythermonomics
```

## Optional Dependencies

- **Documentation:**  
  To build and view the documentation, install with the `docs` extra:
  ```sh
  pip install pythermonomics[docs]
  ```
- **Testing:**  
  To run tests, install with the `tests` extra:
  ```sh
  pip install pythermonomics[tests]
  ```
- **Run Jupyter Notebook example:**  
  To run the notebook example, install with the `notebook` extra:
  ```sh
  pip install pythermonomics[notebook]
  ```

## Install from source

Install the package from the repository root:

```sh
pip install .
```

## Usage

### Command-Line Interface

After installation, use the CLI tool:

```sh
pythermonomics -c config.yml -i sim_data.csv -d deviations/ -t trajectory.yml
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

Browse the full API reference and usage examples at [Docs](https://tno.github.io/pythermonomics/) or build locally:

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

## Contact information

Stephan de Hoop (stephan.dehoop@tno.nl)

## Acknowledgements

This study has been performed as part of the RESULT project (Enhancing REServoirs in Urban deveLopmenT: smart wells and reservoir development). [RESULT](https://www.result-geothermica.eu/home.html) has been subsidized through the ERANET Cofund GEOTHERMICA (EC Project no. 731117), by the Ministry of Economic Affairs and Climate Policy (the Netherlands), Rannis (Iceland) and GSI (Ireland).

<p float="left">
  <img src="docs/logo/RESULT_LOGO.png" alt="RESULT Logo" width="15%" />
  <img src="docs/logo/GEOTHERMICA_LOGO.png" alt="GEOTHERMICA Logo" width="30%" />
</p>

---

For more information, see the [API Reference](docs/index.md) or contact the maintainers.