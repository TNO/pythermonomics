import numpy as np
import pandas as pd
import pytest

from pythermonomics.data.well_results import WellResults


class DummyReservoirParams:
    def __init__(self):
        self.flowrate = 10.0
        self.production_temperature = 120.0
        self.injection_BHP = 100.0
        self.production_BHP = 200.0
        self.injection_temperature = 50


class DummyParameters:
    def __init__(self):
        self.injection_temperature = 60.0


class DummyWellTrajectory:
    platform = [0, 0, 0.0]
    kick_off = [0, 0, 800.0]
    targets = [[800, -500, 2300], [1800, -500, 2400]]


def test_empty_wells_raises():
    res_params = DummyReservoirParams()
    params = DummyParameters()
    nyear = 2
    with pytest.raises(ValueError):
        WellResults({}, res_params, params, nyear)


def test_missing_well_platform_raises():
    wells = {"WELL1": {}, "WELL2": {}}
    res_params = DummyReservoirParams()
    params = DummyParameters()
    nyear = 2
    with pytest.raises(AttributeError):
        _ = WellResults(wells, res_params, params, nyear)


def test_invalid_nyear_raises():
    wells = {"WELL1": {}, "WELL2": {}}
    res_params = DummyReservoirParams()
    params = DummyParameters()
    with pytest.raises(ValueError):
        WellResults(wells, res_params, params, -1)


def test_read_well_path_and_types():
    wells = {
        "WELL1": DummyWellTrajectory,
        "WELL2": DummyWellTrajectory,
    }
    res_params = DummyReservoirParams()
    params = DummyParameters()
    nyear = 2

    wr = WellResults(wells, res_params, params, nyear)
    WXYZ, wells_and_states = wr.read_well_path_and_types()

    assert set(WXYZ.keys()) == set(wells_and_states.keys())
    assert set(wells_and_states.values()) == {"inj", "prod"}
    for arr in WXYZ.values():
        assert isinstance(arr, np.ndarray)


def test_read_wellpaths_production():
    wells = {
        "WELL1": DummyWellTrajectory,
        "WELL2": DummyWellTrajectory,
    }
    res_params = DummyReservoirParams()
    params = DummyParameters()
    nyear = 2

    wr = WellResults(wells, res_params, params, nyear)
    wellRes, wells_and_states, WXYZ = wr.read_wellpaths_production()

    assert isinstance(wellRes, pd.DataFrame)
    assert isinstance(wells_and_states, dict)
    assert isinstance(WXYZ, dict)
    assert all(col in wellRes.columns for col in ["DAYS", "YEARS"])
    for w in wells_and_states:
        assert f"T:{w}" in wellRes.columns


def test_read_well_path_and_types_values():
    wells = {
        "WELL1": DummyWellTrajectory,
        "WELL2": DummyWellTrajectory,
    }
    res_params = DummyReservoirParams()
    params = DummyParameters()
    nyear = 2

    wr = WellResults(wells, res_params, params, nyear)
    WXYZ, wells_and_states = wr.read_well_path_and_types()

    # Check well states
    assert wells_and_states == {"WELL1": "inj", "WELL2": "prod"}
    # Check coordinates
    np.testing.assert_array_equal(
        WXYZ["WELL1"],
        np.array(
            [[0, 0, 0.0], [0, 0, 800.0], [800, -500, 2300], [1800, -500, 2400]],
            dtype="float",
        ),
    )
    np.testing.assert_array_equal(
        WXYZ["WELL2"],
        np.array(
            [[0, 0, 0.0], [0, 0, 800.0], [800, -500, 2300], [1800, -500, 2400]],
            dtype="float",
        ),
    )


def test_read_wellpaths_production_values():
    wells = {
        "WELL1": DummyWellTrajectory,
        "WELL2": DummyWellTrajectory,
    }
    res_params = DummyReservoirParams()
    params = DummyParameters()
    nyear = 2

    wr = WellResults(wells, res_params, params, nyear)
    wellRes, wells_and_states, WXYZ = wr.read_wellpaths_production()

    # There should be 2 years (since years >= 1.0)
    assert list(wellRes["YEARS"]) == [1.0, 2.0]
    # Check temperature columns
    assert all(
        wellRes[f"T:{w}"].iloc[0] == (50.0 if state == "inj" else 120.0)
        for w, state in wells_and_states.items()
    )
    # Check flowrate columns
    qyear = res_params.flowrate * 24 * 365
    # For WWIT:WELL1 (injector), should be 1*qyear and 2*qyear
    assert wellRes["WWIT:WELL1"].iloc[0] == 1 * qyear
    assert wellRes["WWIT:WELL1"].iloc[1] == 2 * qyear
    # For WWPT:WELL2 (producer), should be 1*qyear and 2*qyear
    assert wellRes["WWPT:WELL2"].iloc[0] == 1 * qyear
    assert wellRes["WWPT:WELL2"].iloc[1] == 2 * qyear
    # Check BHP columns
    assert all(wellRes["WBHP:WELL1"] == 100.0)
    assert all(wellRes["WBHP:WELL2"] == 200.0)
    # Check FPR
    assert all(wellRes["FPR"] == 0.5 * (100.0 + 200.0))
