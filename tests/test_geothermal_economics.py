import numpy as np
import pandas as pd
import pytest
from pywellgeo.well_data.dc1dwell import Dc1dwell

from pythermonomics.geothermal_economics import GeothermalEconomics
from tests.conftest import CASHFLOW_DIR, WELL_RESULTS_DIR, dataframes_almost_equal


def run_economics(filename, trajectoryfile=None):
    gt_economics = GeothermalEconomics.from_trajectory(
        filename,
        trajectoryfile=trajectoryfile,
    )
    npv, lcoe, cashflow, simdata, wells, well_results = gt_economics.compute_economics()
    return npv, lcoe, cashflow, simdata, wells, gt_economics, well_results


def test_DC1D(settingfile):
    dc1dsettings = "tests/testdata/config_files/dc1dwell.yml"
    expected_cashflow = pd.read_csv(
        f"{CASHFLOW_DIR}dc1d_well_cashflow_full.csv", index_col=0
    )
    expected_well_results = pd.read_csv(
        f"{WELL_RESULTS_DIR}dc1d_wellresults_full.csv", index_col=0
    )
    dc1dwell = Dc1dwell.from_configfile(dc1dsettings)
    dc1dwell.qvol = -1
    dc1dwell.dp = 30
    g = dc1dwell.get_params()
    g["ahd"] = g["tvd"] + (np.array(g["ahd"]) - np.array(g["tvd"]))
    dc1dwell.update_params(**g)
    dc1dwell.calculateDP_qvol()

    gt_economics = GeothermalEconomics.from_dc1d(settingfile, dc1dsettings, dc1dwell)
    npv, lcoe, cashflow, _, _, well_results = gt_economics.compute_economics()
    ahd = gt_economics.welltrajectory.tw["INJ1"]["welltree"].cumulative_ahd()

    assert gt_economics.power == pytest.approx(3.68, abs=0.01)
    assert gt_economics.cop == pytest.approx(21.3, abs=0.1)
    assert dc1dwell.qvol == pytest.approx(125 / 3600, abs=1e-3)
    assert dc1dwell.dp == pytest.approx(30, abs=1e-1)
    assert ahd == pytest.approx(2140, abs=1.0)
    assert lcoe == pytest.approx(9.96, abs=0.1)
    assert npv == pytest.approx(-6.09e6, abs=1e5)
    assert dataframes_almost_equal(cashflow, expected_cashflow)
    assert dataframes_almost_equal(well_results, expected_well_results)


@pytest.mark.parametrize(
    "trajectoryfile, expected_ahd, expected_cost, expected_lcoe, expected_npv, expected_cashflow, expected_well_results",
    [
        (
            "tests/testdata/config_files/inputsStandard.yml",
            2665,
            10.6e6,
            5.15,
            -0.29e6,
            "standard_trajectory_file_cashflow.csv",
            "standard_trajectory_file_wellresults.csv",
        ),
        (
            None,
            3577,
            15.9e6,
            5.88,
            -4.12e6,
            "no_trajectory_file_cashflow.csv",
            "no_trajectory_file_wellresults.csv",
        ),
    ],
)
def test_cases(
    settingfile,
    trajectoryfile,
    expected_ahd,
    expected_cost,
    expected_lcoe,
    expected_npv,
    expected_cashflow,
    expected_well_results,
):
    expected_cashflow = pd.read_csv(f"{CASHFLOW_DIR}{expected_cashflow}", index_col=0)
    expected_well_results = pd.read_csv(
        f"{WELL_RESULTS_DIR}{expected_well_results}", index_col=0
    )
    npv, lcoe, cashflow, _, _, gt_economics, well_results = run_economics(
        settingfile, trajectoryfile=trajectoryfile
    )
    ahd = gt_economics.welltrajectory.tw["INJ1"]["welltree"].cumulative_ahd()
    cost = gt_economics.wellcostmodel.compute_costs()

    assert ahd == pytest.approx(expected_ahd, abs=1.0)
    assert cost == pytest.approx(expected_cost, abs=1e5)
    assert lcoe == pytest.approx(expected_lcoe, abs=0.02)
    assert npv == pytest.approx(expected_npv, abs=1e5)
    assert dataframes_almost_equal(cashflow, expected_cashflow)
    assert dataframes_almost_equal(well_results, expected_well_results)


@pytest.mark.parametrize(
    "trajectoryfile, expected_npv, expected_lcoe, expected_cashflow, expected_well_results",
    [
        (
            "tests/testdata/trajectory_files/inputsDetailedTNOhor.yml",
            -5890006,
            6.19,
            "detailed_tno_horizontal_cashflow.csv",
            "detailed_tno_horizontal_wellresults.csv",
        ),
    ],
)
def test_multilateral_variants(
    settingfile,
    trajectoryfile,
    expected_npv,
    expected_lcoe,
    expected_cashflow,
    expected_well_results,
):
    expected_cashflow = pd.read_csv(f"{CASHFLOW_DIR}{expected_cashflow}", index_col=0)
    expected_well_results = pd.read_csv(
        f"{WELL_RESULTS_DIR}{expected_well_results}", index_col=0
    )
    npv, lcoe, cashflow, _, _, _, well_results = run_economics(
        settingfile, trajectoryfile=trajectoryfile
    )
    assert npv == pytest.approx(expected_npv, abs=1000.0)
    assert lcoe == pytest.approx(expected_lcoe, abs=0.02)
    assert dataframes_almost_equal(cashflow, expected_cashflow)
    assert dataframes_almost_equal(well_results, expected_well_results)
