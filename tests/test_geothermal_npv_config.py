import pytest

from pythermonomics.config.geothermal_economics_config import (
    GeothermalEconomicsConfig,
)
from pythermonomics.config.reservoir_simulation_parameters import (
    ReservoirSimulationParameters,
)


def minimal_techno_eco_params():
    return {
        "loadhours": 6000,
        "wellcost_scaling": 1.0,
        "well_curvfac": 1.0,
        "wellcost_base": 100000,
        "wellcost_linear": 500,
        "wellcost_cube": 0.1,
        "pump_efficiency": 0.6,
        "pump_cost": 100000,
        "pump_life": 5,
        "CAPEX_base": 1000000,
        "CAPEX_variable": 1000,
        "CAPEX_contingency": 0.1,
        "OPEX_base": 10000,
        "OPEX_variable": 100,
        "OPEX_variable_produced": 0.1,
        "equity_share": 0.2,
        "loan_nyear": 10,
        "loan_rate": 0.05,
        "discount_rate": 0.1,
        "inflation_rate": 0.02,
        "tax_rate": 0.25,
        "tax_depreciation_nyear": 10,
        "heat_price": 5.0,
        "heat_price_feedin": 5.0,
        "electricity_price": 8.0,
        "lifecycle_years": 1.0,
        "subsidy_years": 1.0,
    }


def minimal_reservoir_simulation_parameters():
    return {
        "injection_temperature": 50,
        "salinity": 100000,
        "production_temperature": 90,
        "injection_BHP": 260,
        "production_BHP": 200,
        "flowrate": 400,
    }


def minimal_energy_loss_parameters():
    return {
        "well_roughness": 0.1,
        "well_tubing": 8.5,
        "useheatloss": True,
        "tsurface": 10.0,
        "tgrad": 0.03,
    }


def minimal_config_dict():
    return {
        "techno_economic_parameters": minimal_techno_eco_params(),
        "reservoir_simulation_parameters": minimal_reservoir_simulation_parameters(),
        "energy_loss_parameters": minimal_energy_loss_parameters(),
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
    }


def test_geothermal_economics_config_valid():
    cfg = GeothermalEconomicsConfig(**minimal_config_dict())
    assert cfg.techno_eco_param.lifecycle_years == 1
    assert cfg.reservoir_parameters.injection_temperature == 50
    assert cfg.reservoir_parameters.production_temperature == 90
    assert "INJ1" in cfg.well_trajectories


def test_geothermal_economics_config_alias_resparam():
    # Should work with 'resparam' as alias for 'reservoir_parameters'
    cfg = GeothermalEconomicsConfig(**minimal_config_dict())
    assert isinstance(cfg.reservoir_parameters, ReservoirSimulationParameters)
    assert cfg.reservoir_parameters.production_BHP == 200


def test_geothermal_economics_config_missing_required():
    # Remove a required field
    config = minimal_config_dict()
    del config["techno_economic_parameters"]
    with pytest.raises(Exception):
        GeothermalEconomicsConfig(**config)


def test_geothermal_economics_config_invalid_type():
    config = minimal_config_dict()
    config["techno_economic_parameters"]["lifecycle_years"] = "not_an_int"
    with pytest.raises(Exception):
        GeothermalEconomicsConfig(**config)


def test_geothermal_economics_config_load_from_file(tmp_path):
    import yaml

    config = minimal_config_dict()
    file = tmp_path / "test_config.yml"
    with open(file, "w") as f:
        yaml.dump(config, f)
    cfg = GeothermalEconomicsConfig.load_from_file(str(file))
    assert cfg.techno_eco_param.lifecycle_years == 1
    assert cfg.reservoir_parameters.injection_temperature == 50


def test_missing_parameters_section():
    config = minimal_config_dict()
    config.pop("techno_economic_parameters")
    with pytest.raises(Exception) as excinfo:
        GeothermalEconomicsConfig(**config)
    assert "techno_economic_parameters" in str(excinfo.value)


def test_missing_reservoir_parameters_section():
    config = minimal_config_dict()
    config.pop("reservoir_simulation_parameters")
    # Should still work, as reservoir_parameters is optional, but let's check
    cfg = GeothermalEconomicsConfig(**config)
    assert cfg.reservoir_parameters is None


def test_missing_well_trajectories_section():
    config = minimal_config_dict()
    config.pop("well_trajectories")
    # Should still work, as reservoir_parameters is optional, but let's check
    cfg = GeothermalEconomicsConfig(**config)
    assert cfg.well_trajectories is None


def test_wrong_type_for_parameters():
    config = minimal_config_dict()
    config["techno_economic_parameters"] = "not_a_dict"
    with pytest.raises(Exception) as excinfo:
        GeothermalEconomicsConfig(**config)
    assert "parameters" in str(excinfo.value)


def test_missing_required_nested_field():
    config = minimal_config_dict()
    # Remove a required field from parameters
    del config["reservoir_simulation_parameters"]["injection_temperature"]
    with pytest.raises(Exception) as excinfo:
        GeothermalEconomicsConfig(**config)
    assert "injection_temperature" in str(excinfo.value)


def test_invalid_type_in_nested_parameters():
    config = minimal_config_dict()
    config["reservoir_simulation_parameters"]["injection_temperature"] = "not_a_float"
    with pytest.raises(Exception) as excinfo:
        GeothermalEconomicsConfig(**config)
    assert "injection_temperature" in str(excinfo.value)


def test_invalid_type_in_nested_reservoir_parameters():
    config = minimal_config_dict()
    config["reservoir_simulation_parameters"]["production_BHP"] = "not_a_float"
    with pytest.raises(Exception) as excinfo:
        GeothermalEconomicsConfig(**config)
    assert "production_BHP" in str(excinfo.value)
