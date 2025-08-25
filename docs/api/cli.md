# pythermonomics.cli

**Module:** `pythermonomics.cli`

The CLI (`pythermonomics.cli`) is the main entry point for running geothermal economics calculations from the command line.

---

## Purpose

- Provides a user-friendly command-line interface for NPV and LCOE calculations.
- Allows users to specify configuration, simulation, deviation, and trajectory files.
- Outputs results to the console and optionally saves them to disk.

---

## Main Function

### `main()`

Parses command-line arguments, sets up logging, and runs the NPV/LCOE calculation workflow.

#### Arguments

- `-c, --config`: Path to YAML configuration file (required)
- `-i, --sim-data`: Path to simulation data CSV file (optional)
- `-d, --dev-files`: Path to directory with deviation files (optional)
- `-t, --trajectoryfile`: Path to well trajectory file (optional)
- `--no-save`: Do not save results to files
- `-v, --verbose`: Enable verbose output

---

## Usage

After installing the package, run:

```sh
python -m pythermonomics.cli -c config.yml -i sim_data.csv -d deviations/ -t trajectory.yml
```

Or, if installed as a script:

```sh
geothermal-calc -c config.yml -i sim_data.csv -d deviations/ -t trajectory.yml
```

---

## Example Output

- NPV and LCOE printed to the console
- Results saved to `npv`, `lcoe`, and `cashflow.csv` files (unless `--no-save` is specified)

---

## API Reference

See [GeothermalEconomics](geothermal_economics.md) for the main API.

---

## Related Modules

- [GeothermalEconomicsConfig](config/GeothermalEconomicsConfig.md)
- [EnergyCalculator](energy_model/EnergyCalculator.md)
- [EconomicsCalculator](npv_model/EconomicsCalculator.md)