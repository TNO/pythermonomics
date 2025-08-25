import pandas as pd
import pytest

from pythermonomics.geothermal_economics import GeothermalEconomics
from tests.conftest import CASHFLOW_DIR, WELL_RESULTS_DIR, dataframes_almost_equal


def run_lcoe(filename, summary_file, deviation_files_dir):
    gt_economics = GeothermalEconomics.from_summary_deviation_file(
        filename,
        summary_file=summary_file,
        deviation_files_dir=deviation_files_dir,
    )
    npv, lcoe, cashflow, simdata, wells, well_results = gt_economics.compute_economics()
    return npv, lcoe, cashflow, simdata, wells, gt_economics, well_results


def test_run_lcoe_with_summary_and_dev():
    filename = "tests/testdata/config_files/economics_input.yml"
    summary_file = "tests/testdata/summary_files/summary_data_test.csv"
    deviation_files_dir = "tests/testdata/well_paths"
    expected_cashflow = pd.read_csv(f"{CASHFLOW_DIR}expected_cashflow.csv", index_col=0)
    expected_wellresults = pd.read_csv(
        f"{WELL_RESULTS_DIR}expected_wellresults.csv", index_col=0
    )

    npv, lcoe, cashflow, simdata, wells, gt_economics, well_results = run_lcoe(
        filename, summary_file=summary_file, deviation_files_dir=deviation_files_dir
    )

    assert npv == pytest.approx(-28681206, abs=1000.0)
    assert lcoe == pytest.approx(6.3465, abs=1e-3)
    assert isinstance(cashflow, pd.DataFrame)
    assert isinstance(simdata, pd.DataFrame)
    assert isinstance(wells, dict)
    assert isinstance(gt_economics, GeothermalEconomics)
    assert dataframes_almost_equal(cashflow, expected_cashflow)
    assert dataframes_almost_equal(well_results, expected_wellresults)
