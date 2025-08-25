import os
import tempfile

import numpy as np
import pytest

from pythermonomics.data.read_deviation_file import DeviationFileReader


def make_deviation_file(content: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, mode="w", suffix=".dev")
    tmp.write(content)
    tmp.close()
    return tmp.name


def test_read_valid_deviation_file():
    content = (
        "WELLNAME: 'INJ1'\n"
        "#       X           Y      TVDMSL       MDMSL\n"
        "  2553.32     2277.76        0.00        0.00\n"
        "  2553.28     2277.94        5.00        5.00\n"
        "  2485.83     5155.36     2854.80     5973.30\n"
        "-999\n"
    )
    path = make_deviation_file(content)
    reader = DeviationFileReader(path)
    assert reader.well_name == "INJ1"
    assert reader.deviation_data.shape == (3, 4)
    np.testing.assert_allclose(reader.deviation_data[0], [2553.32, 2277.76, 0.0, 0.0])
    os.remove(path)


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        DeviationFileReader("nonexistent_file.dev")


def test_invalid_line_format_raises():
    content = (
        "WELLNAME: 'INJ1'\n"
        "2553.32 2277.76 0.00\n"  # Only 3 columns, should be 4
        "-999\n"
    )
    path = make_deviation_file(content)
    with pytest.raises(ValueError, match="Invalid line format"):
        DeviationFileReader(path)
    os.remove(path)


def test_invalid_coordinate_data_raises():
    content = (
        "WELLNAME: 'INJ1'\n"
        "2553.32 2277.76 0.00 abc\n"  # Non-numeric value
        "-999\n"
    )
    path = make_deviation_file(content)
    with pytest.raises(ValueError, match="Invalid coordinate data"):
        DeviationFileReader(path)
    os.remove(path)


def test_no_valid_well_data_raises():
    content = "# Just a comment\n-999\n"
    path = make_deviation_file(content)
    with pytest.raises(ValueError, match="No valid well data found"):
        DeviationFileReader(path)
    os.remove(path)
