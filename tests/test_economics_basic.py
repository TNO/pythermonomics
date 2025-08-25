import pandas as pd
import pytest

from pythermonomics.geothermal_economics import GeothermalEconomics
from tests.conftest import CASHFLOW_DIR, WELL_RESULTS_DIR, dataframes_almost_equal


def test_geothermal_economics_from_dc1d(minimal_settings):
    # Mock a Dc1dwell object with required attributes
    class DummyDc1d:
        temp = [60, 120]
        salinity = [10000, 10000]
        rw = [0.1, 0.1]
        roughness = 0.05
        qvol = 0.05
        dpres = 30

    expected_cashflow = pd.read_csv(
        f"{CASHFLOW_DIR}dc1d_well_cashflow_simple.csv", index_col=0
    )
    expected_wellresults = pd.read_csv(
        f"{WELL_RESULTS_DIR}dc1d_well_wellresults_simple.csv", index_col=0
    )

    dc1d = DummyDc1d()
    economics = GeothermalEconomics.from_dc1d(minimal_settings, None, dc1d)
    assert hasattr(economics, "simresults")
    assert hasattr(economics, "welltrajectory")
    assert hasattr(economics, "wellcostmodel")
    # Check that simresults contains a DataFrame with expected columns
    assert hasattr(economics.simresults, "wellRes")
    assert "YEARS" in economics.simresults.wellRes.columns

    npv, lcoe_val, cashflow, *_, well_results = economics.compute_economics()
    assert npv == pytest.approx(-4535187, abs=1000.0)
    assert lcoe_val == pytest.approx(15.05, abs=0.01)
    assert dataframes_almost_equal(cashflow, expected_cashflow)
    assert dataframes_almost_equal(well_results, expected_wellresults)


def test_geothermal_economics_npv_lcoe_minial_settings(minimal_settings):
    economics = GeothermalEconomics.from_trajectory(minimal_settings, None)
    expected_cashflow = pd.read_csv(
        f"{CASHFLOW_DIR}minimal_example_cashflow.csv", index_col=0
    )
    expected_wellresults = pd.read_csv(
        f"{WELL_RESULTS_DIR}minimal_example_wellresults.csv", index_col=0
    )

    npv, lcoe_val, cashflow, *_, well_results = economics.compute_economics()
    assert npv == pytest.approx(-4556437, abs=1000.0)
    assert lcoe_val == pytest.approx(11.92, abs=0.01)
    assert dataframes_almost_equal(cashflow, expected_cashflow)
    assert dataframes_almost_equal(well_results, expected_wellresults)
