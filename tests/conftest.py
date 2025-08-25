import pandas as pd
import pytest
import yaml

CASHFLOW_DIR = "tests/testdata/economic_dataframes/"
WELL_RESULTS_DIR = "tests/testdata/well_results_dataframes/"


@pytest.fixture
def settingfile():
    return "tests/testdata/config_files/npv_thermogis2024.yml"


@pytest.fixture
def input_dir():
    return "tests/testdata"


@pytest.fixture
def output_dir(tmp_path):
    return tmp_path  # or use './output' if you want to persist


@pytest.fixture
def minimal_settings(tmp_path):
    settings = {
        "energy_loss_parameters": {
            "well_roughness": 0.138,
            "well_tubing": 8.5,
            "useheatloss": True,
            "tsurface": 10.0,
            "tgrad": 0.031,
        },
        "reservoir_simulation_parameters": {
            "injection_temperature": 50,
            "salinity": 140000,
            "production_temperature": 90,
            "injection_BHP": 260,
            "production_BHP": 200,
            "flowrate": 400,
        },
        "well_trajectories": {
            "INJ1": {
                "platform": [0, 0, 0.0],
                "kick_off": [0, 0, 800.0],
                "targets": [[800, 500, 2300], [1800, 500, 2400]],
            },
            "PRD1": {
                "platform": [0, 0, 0.0],
                "kick_off": [0, 0, 800.0],
                "targets": [[800, 500, 2300], [1800, 500, 2400]],
            },
        },
        "techno_economic_parameters": {
            "loadhours": 6000,
            "wellcost_scaling": 1.5,
            "well_curvfac": 1.00,
            "wellcost_base": 250e3,
            "wellcost_linear": 700,
            "wellcost_cube": 0.2,
            "pump_efficiency": 0.6,
            "pump_cost": 0.5e6,
            "pump_life": 5,
            "CAPEX_base": 3e6,
            "CAPEX_variable": 300,
            "CAPEX_contingency": 0.15,
            "OPEX_base": 0,
            "OPEX_variable": 100,
            "OPEX_variable_produced": 0.19,
            "equity_share": 0.2,
            "loan_nyear": 15,
            "loan_rate": 0.05,
            "discount_rate": 0.145,
            "inflation_rate": 0.015,
            "tax_rate": 0.25,
            "tax_depreciation_nyear": 15,
            "heat_price": 5.1,
            "heat_price_feedin": 5.1,
            "electricity_price": 8,
            "lifecycle_years": 1,
            "subsidy_years": 1,
        },
    }
    settings_file = tmp_path / "settings.yml"
    with open(settings_file, "w") as f:
        yaml.dump(settings, f)
    return str(settings_file)


def dataframes_almost_equal(df1, df2, tol=1e-5):
    try:
        pd.testing.assert_frame_equal(df1, df2, atol=tol, rtol=tol)
        return True
    except AssertionError as e:
        print(e)
        return False
