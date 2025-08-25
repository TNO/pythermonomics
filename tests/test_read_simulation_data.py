import os
import tempfile
from tempfile import NamedTemporaryFile

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from pythermonomics.data.read_sim_data_from_csv import (
    SimulationDataReader,
    WellState,
)


@pytest.fixture
def valid_csv_file():
    data = {
        "DATES": [2020, 2021],
        "YEARS": [0, 1],
        "WTPCHEA:INJ1": [0, 0],
        "WTPCHEA:PROD1": [1.1, 1.2],
        "WTICHEA:INJ1": [2.1, 2.2],
        "WTICHEA:PROD1": [0, 0],
        "FPR": [3.1, 3.2],
        "WWPR:INJ1": [0, 0],
        "WWPR:PROD1": [0, 0],
        "WWIR:INJ1": [0, 0],
        "WWIR:PROD1": [0, 0],
        "WBHP:INJ1": [0, 0],
        "WBHP:PROD1": [0, 0],
        "WWPT:INJ1": [0, 0],
        "WWPT:PROD1": [0, 0],
        "WWIT:INJ1": [0, 0],
        "WWIT:PROD1": [0, 0],
        "WSTAT:INJ1": [3.0, 2.0],
        "WSTAT:PROD1": [1.0, 1.0],
    }
    df = pd.DataFrame(data)
    with NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name)
        yield tmp.name
    os.remove(tmp.name)


@pytest.fixture
def invalid_csv_file():
    data = {
        "YEARS": [2020, 2021],
        "WTPCHEA": [1.1, 1.2],
        "FPR": [3.1, 3.2],  # Missing other required columns
    }
    df = pd.DataFrame(data)
    with NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as tmp:
        df.to_csv(tmp.name)
        yield tmp.name
    os.remove(tmp.name)


def create_temp_csv(content: str) -> str:
    """Helper function to create a temporary CSV file."""
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w")
    tmp.write(content)
    tmp.close()
    return tmp.name


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        SimulationDataReader("non_existent_file.csv")


def test_missing_required_keys(invalid_csv_file):
    with pytest.raises(KeyError) as exc_info:
        _ = SimulationDataReader(invalid_csv_file)
    assert "Missing keys in data:" in str(exc_info.value)


def test_successful_data_extraction(valid_csv_file):
    reader = SimulationDataReader(valid_csv_file)
    result = reader.get_relevant_simulation_results()
    assert list(result.columns) == reader.REQUIRED_KEYS
    assert result.shape[0] == 2


def test_reading_summary_data():
    csv_file = "tests/testdata/summary_files/summary_data_test.csv"
    expected = pd.read_csv(
        "tests/testdata/summary_files/simulation_time_series.csv", index_col=0
    )

    reader = SimulationDataReader(csv_file)
    result = reader.get_relevant_simulation_results()
    assert list(result.columns) == reader.REQUIRED_KEYS
    assert not result.empty  # Ensure that the DataFrame is not empty
    assert_frame_equal(result, expected, check_dtype=False, check_like=True, atol=1e-6)


def test_successful_data_extraction_with_valid_wells():
    content = (
        "DATES,YEARS,FPR,WTPCHEA:INJ1,WTICHEA:INJ1,WWPR:INJ1,WWIR:INJ1,WBHP:INJ1,WWPT:INJ1,WWIT:INJ1,"
        "WSTAT:INJ1,WSTAT:PRD1,WTPCHEA:PRD1,WTICHEA:PRD1,WWPR:PRD1,WWIR:PRD1,WBHP:PRD1,WWPT:PRD1,WWIT:PRD1\n"
        "2020,0,100,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\n"
    )
    path = create_temp_csv(content)
    reader = SimulationDataReader(path)
    df = reader.get_relevant_simulation_results()
    assert not df.empty
    assert all(col in df.columns for col in reader.REQUIRED_KEYS)
    os.remove(path)


def test_unsuccessful_data_extraction_missing_keyword_for_one_well():
    content = (
        "DATES,YEARS,FPR,WTICHEA:INJ1,WWPR:INJ1,WWIR:INJ1,WBHP:INJ1,WWPT:INJ1,WWIT:INJ1,"
        "WSTAT:INJ1,WSTAT:PRD1,WTPCHEA:PRD1,WTICHEA:PRD1,WWPR:PRD1,WWIR:PRD1,WBHP:PRD1,WWPT:PRD1,WWIT:PRD1\n"
        "2020,0,100,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1\n"
    )
    path = create_temp_csv(content)
    with pytest.raises(KeyError) as excinfo:
        SimulationDataReader(path)
    assert excinfo.value.args[0] == "Missing keywords per well: {'INJ1': ['WTPCHEA']}"


def make_csv(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv", mode="w")
    tmp.write(content)
    tmp.close()
    return tmp.name


def test_extract_well_names_from_csv():
    content = (
        "DATES,YEARS,FPR,WTPCHEA:INJ1,WTICHEA:INJ1,WWPR:INJ1,WWIR:INJ1,WBHP:INJ1,WWPT:INJ1,WWIT:INJ1,"
        "WTPCHEA:PRD1,WTICHEA:PRD1,WWPR:PRD1,WWIR:PRD1,WBHP:PRD1,WWPT:PRD1,WWIT:PRD1,WSTAT:INJ1,WSTAT:PRD1\n"
        "2020,0,100,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1\n"
    )
    path = make_csv(content)
    reader = SimulationDataReader(path)
    assert set(reader.WELL_NAMES) == {"INJ1", "PRD1"}
    os.remove(path)


def test_extract_well_states_final_timestep():
    content = (
        "DATES,YEARS,FPR,WTPCHEA:INJ1,WTICHEA:INJ1,WWPR:INJ1,WWIR:INJ1,WBHP:INJ1,WWPT:INJ1,WWIT:INJ1,"
        "WTPCHEA:PRD1,WTICHEA:PRD1,WWPR:PRD1,WWIR:PRD1,WBHP:PRD1,WWPT:PRD1,WWIT:PRD1,WSTAT:INJ1,WSTAT:PRD1\n"
        "2020,0,100,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1\n"
        "2021,1,101,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,2\n"
    )
    path = make_csv(content)
    reader = SimulationDataReader(path)
    # Last row: WSTAT:INJ1=1 (prod), WSTAT:PRD1=2 (inj)
    assert reader.WELL_STATES["INJ1"] == WellState.PRODUCTION
    assert reader.WELL_STATES["PRD1"] == WellState.INJECTION
    os.remove(path)


def test_add_single_temperature_column():
    content = (
        "DATES,YEARS,FPR,WTPCHEA:INJ1,WTICHEA:INJ1,WWPR:INJ1,WWIR:INJ1,WBHP:INJ1,WWPT:INJ1,WWIT:INJ1,"
        "WTPCHEA:PRD1,WTICHEA:PRD1,WWPR:PRD1,WWIR:PRD1,WBHP:PRD1,WWPT:PRD1,WWIT:PRD1,WSTAT:INJ1,WSTAT:PRD1\n"
        "2020,0,100,11,12,13,14,15,16,17,21,22,23,24,25,26,27,2,1\n"
    )
    path = make_csv(content)
    reader = SimulationDataReader(path, add_single_temperature_column=True)
    # INJ1 is inj, PRD1 is prod
    assert "T:INJ1" in reader.data.columns
    assert "T:PRD1" in reader.data.columns
    assert reader.data["T:INJ1"].iloc[0] == 12
    assert reader.data["T:PRD1"].iloc[0] == 21
    os.remove(path)


def test_filter_out_whole_years(valid_csv_file):
    # Two years, but only one row should be kept per year
    valid_csv = pd.read_csv(valid_csv_file, index_col=0)
    duplicated_rows = pd.concat([valid_csv.iloc[[0]]] * 5, ignore_index=True)
    duplicated_rows["DATES"] = [
        "2000-01-01",
        "2000-05-01",
        "2001-01-01",
        "2001-05-01",
        "2002-01-01",
    ]
    duplicated_rows["YEARS"] = [
        1.01,
        1.45,
        2.01,
        2.45,
        3.01,
    ]
    path = make_csv(duplicated_rows.to_csv(index=False))
    reader = SimulationDataReader(path)
    # Should keep one row per year
    assert len(reader.data) == 3
    assert abs(reader.data["YEARS"].iloc[0] - 1) < 0.01
    assert abs(reader.data["YEARS"].iloc[1] - 2) < 0.01
    assert abs(reader.data["YEARS"].iloc[2] - 3) < 0.01
    os.remove(path)


def test_missing_columns_raises():
    content = "DATES,YEARS,FPR,WTICHEA:INJ1,WSTAT:INJ1\n2020,0,100,11,2\n"
    path = make_csv(content)
    with pytest.raises(
        KeyError, match="Missing keys in data: WBHP, WTPCHEA, WWIR, WWIT, WWPR, WWPT"
    ):
        SimulationDataReader(path)
    os.remove(path)
