import subprocess

CONFIG_OPM_RUN = "tests/testdata/config_files/economics_input.yml"
DUMMY_SIM_DATA = "tests/testdata/summary_files/summary_data_test.csv"
DUMMY_DEV_DIR = "tests/testdata/well_paths"


def test_cli_help():
    result = subprocess.run(
        ["pythermonomics", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "Geothermal Economics Calculator" in result.stdout


def test_cli_minimal_required(settingfile):
    result = subprocess.run(
        ["pythermonomics", "-c", settingfile, "--no-save", "--verbose"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "NPV=" in result.stderr


def test_cli_with_all_args():
    result = subprocess.run(
        [
            "pythermonomics",
            "-c",
            CONFIG_OPM_RUN,
            "-i",
            DUMMY_SIM_DATA,
            "-d",
            DUMMY_DEV_DIR,
            "--no-save",
            "--verbose",
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "LCOE=" in result.stderr


def test_cli_invalid_config():
    result = subprocess.run(
        ["pythermonomics", "-c", "nonexistent.yml"], capture_output=True, text=True
    )
    assert result.returncode != 0
    assert "No such file or directory" in result.stderr or "Error" in result.stderr
