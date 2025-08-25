import numpy as np
import pandas as pd
import pytest

from pythermonomics.data.simulation_model_results import SimulationModelResults


class DummySimReader:
    WELL_STATES = {"W1": "prod"}
    WELL_NAMES = ["W1"]

    def __init__(self, *args, **kwargs):
        pass

    def get_relevant_simulation_results(self):
        # Minimal DataFrame with required columns
        return pd.DataFrame(
            {
                "YEARS": [1.0, 2.0],
                "DATES": ["2021-01-01 00:00:00", "2022-01-01 00:00:00"],
            }
        )


class DummyDevReader:
    def __init__(self, *args, **kwargs):
        self.deviation_data = np.array([[0, 0, 0], [1, 1, 1]])


@pytest.fixture
def patch_sim_and_dev(monkeypatch):
    monkeypatch.setattr(
        "pythermonomics.data.simulation_model_results.SimulationDataReader",
        DummySimReader,
    )
    monkeypatch.setattr(
        "pythermonomics.data.simulation_model_results.DeviationFileReader",
        DummyDevReader,
    )


def test_missing_summary_file_raises(patch_sim_and_dev, tmp_path):
    with pytest.raises(FileNotFoundError, match="Summary file .* does not exist."):
        SimulationModelResults(
            summary_file="not_a_file.csv",
            path_deviation_files="not_a_path",
        )


def test_wrong_dev_path_raises(patch_sim_and_dev, tmp_path):
    summary_file = tmp_path / "summary.csv"
    summary_file.write_text("dummy")
    with pytest.raises(
        FileNotFoundError, match="Path to deviation files .* does not exist"
    ):
        SimulationModelResults(
            summary_file=summary_file,
            path_deviation_files="not_a_path",
        )


def test_not_enough_dev_files_raises(patch_sim_and_dev, tmp_path):
    summary_file = tmp_path / "summary.csv"
    summary_file.write_text("dummy")
    dev_dir = tmp_path / "dev"
    dev_dir.mkdir()
    # Add two dummy files to pass the deviation file count check
    (dev_dir / "W1.dev").write_text("dummy")
    with pytest.raises(
        ValueError,
        match=f"At least two deviation files are required in path {str(dev_dir)}",
    ):
        SimulationModelResults(
            summary_file=str(summary_file),
            path_deviation_files=str(dev_dir),
        )


def test_successful_creation(patch_sim_and_dev, tmp_path):
    summary_file = tmp_path / "summary.csv"
    summary_file.write_text("dummy")
    dev_dir = tmp_path / "dev"
    dev_dir.mkdir()
    (dev_dir / "W1.dev").write_text("dummy")
    (dev_dir / "W2.dev").write_text("dummy")
    ewr = SimulationModelResults(
        summary_file=str(summary_file),
        path_deviation_files=str(dev_dir),
    )
    assert isinstance(ewr.wellRes, pd.DataFrame)
    assert isinstance(ewr.wells_and_states, dict)
    assert isinstance(ewr.WXYZ, dict)
    assert "W1" in ewr.WXYZ
    assert isinstance(ewr.WXYZ["W1"], np.ndarray)
