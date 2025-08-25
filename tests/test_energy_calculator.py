import numpy as np
import pandas as pd
import pytest

from pythermonomics.energy_model.energy_calculator import EnergyCalculator


class DummyResParam:
    injection_temperature = 50
    salinity = 140000


class DummyEnergyLoss:
    well_tubing = 8.5
    well_roughness = 0.138
    useheatloss = False


class DummyEconomics:
    loadhours = 6000
    pump_efficiency = 0.6


class DummyEconomicsConfig:
    reservoir_parameters: DummyResParam
    energy_loss_parameters: DummyEnergyLoss
    techno_eco_param: DummyEconomics


class DummyTrajectoryInput:
    dp_frictionprod = 1.0
    dpSyphon = 0.5
    dp_frictioninj = 0.8

    def friction_all(self, *args, **kwargs):
        pass

    def temploss_all(self, *args, **kwargs):
        return [0, 0]


class DummyWellTrajectory:
    trajectoryinput = DummyTrajectoryInput()


class DummySimResults:
    wells_and_states = {"P1": "prod", "I1": "inj"}
    wellRes = pd.DataFrame(
        {
            "DAYS": [0, 365],
            "YEARS": [0, 1],
            "FPR": [230, 230],
            "T:P1": [120, 120],
            "T:I1": [50, 50],
            "WWPT:P1": [0, 100000],
            "WWIT:I1": [0, 100000],
            "WBHP:P1": [200, 200],
            "WBHP:I1": [260, 260],
        }
    )


@pytest.fixture
def dummy_lcoe():
    class DummyLcoe:
        simresults = DummySimResults()
        economics_config = DummyEconomicsConfig()
        economics_config.reservoir_parameters = DummyResParam()
        economics_config.energy_loss_parameters = DummyEnergyLoss()
        economics_config.techno_eco_param = DummyEconomics()
        welltrajectory = DummyWellTrajectory()

    return DummyLcoe()


def test_compute_energy_basic(dummy_lcoe):
    calc = EnergyCalculator(dummy_lcoe)
    # Prepare a minimal cashflow DataFrame
    cashflow = pd.DataFrame({"dTime": [1, 364]})
    result, nwp, nwi = calc.compute_energy(cashflow)
    # Assert structure
    assert isinstance(result, pd.DataFrame)
    assert "enTemp" in result.columns
    assert "enProd" in result.columns
    assert "enInj" in result.columns
    assert "enPower[MW]" in result.columns
    assert "enPowercons[MW]" in result.columns
    assert "COP" in result.columns
    # Assert values are finite and reasonable
    assert np.all(np.isfinite(result["enTemp"]))
    assert np.all(result["enTemp"] >= 0)
    assert np.all(result["enProd"] >= 0)
    assert np.all(result["enInj"] >= 0)
    assert np.all(result["enPower[MW]"] >= 0)
    assert np.all(result["enPowercons[MW]"] >= 0)
    # Assert well counts
    assert nwp == 1
    assert nwi == 1
    assert result["COP"][1] == pytest.approx(25.65, abs=0.1)
    assert result["enPower[MW]"][1] == pytest.approx(0.84, abs=0.1)
    assert result["enPowercons[MW]"][1] == pytest.approx(0.032, abs=0.01)
    assert result["enTemp"][1] == pytest.approx(18231, abs=100.0)
    assert result["enProd"][1] == pytest.approx(359, abs=1.0)
    assert result["enInj"][1] == pytest.approx(351, abs=1.0)
