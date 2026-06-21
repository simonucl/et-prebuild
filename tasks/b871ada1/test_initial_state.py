# test_initial_state.py
#
# This test-suite validates that the operating system / filesystem is in the
# expected *initial* state before the student performs any actions.
#
# It checks:
#   • Presence and permissions of the data and output directories.
#   • Presence and exact content of the three source CSV files.
#   • That the output directory is still empty (no artefacts yet).

import os
import stat
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "iot_deploy")
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

SENSORS_CSV = os.path.join(DATA_DIR, "sensors.csv")
CONFIG_CSV = os.path.join(DATA_DIR, "config.csv")
CONNECTIVITY_CSV = os.path.join(DATA_DIR, "connectivity.csv")


def _assert_perm_755(path: str):
    mode = os.stat(path).st_mode & 0o777
    assert mode == 0o755, f"Expected permissions 755 on '{path}', found {oct(mode)}"


def test_data_directory_exists_and_permissions():
    assert os.path.isdir(DATA_DIR), f"Required directory '{DATA_DIR}' is missing."
    _assert_perm_755(DATA_DIR)


def test_output_directory_exists_permissions_and_empty():
    assert os.path.isdir(OUTPUT_DIR), f"Required directory '{OUTPUT_DIR}' is missing."
    _assert_perm_755(OUTPUT_DIR)

    # The directory must be empty at the start.
    contents = os.listdir(OUTPUT_DIR)
    assert (
        len(contents) == 0
    ), f"Output directory '{OUTPUT_DIR}' should be empty initially, found: {contents}"


@pytest.mark.parametrize(
    "csv_file, expected_lines",
    [
        (
            SENSORS_CSV,
            [
                "device_id,sensor_type,firmware_version,calibration_date",
                "D-1001,temperature,1.4.2,2022-11-01",
                "D-1002,humidity,2.0.0,2023-01-15",
                "D-1003,pressure,1.2.1,2022-07-22",
                "D-1004,temperature,1.4.2,2022-12-10",
                "D-1005,humidity,2.0.1,2023-02-05",
            ],
        ),
        (
            CONFIG_CSV,
            [
                "device_id,edge_location,cpu_arch,memory",
                "D-1001,EdgeRack-01,arm64,2048",
                "D-1002,EdgeRack-02,arm64,2048",
                "D-1003,EdgeRack-01,armv7,1024",
                "D-1004,EdgeRack-02,arm64,2048",
                "D-1005,EdgeRack-03,armv7,1024",
            ],
        ),
        (
            CONNECTIVITY_CSV,
            [
                "device_id,ip_address,mac_address,last_seen",
                "D-1001,10.0.0.11,00:1A:C2:7B:00:11,2023-03-12T09:45:02Z",
                "D-1002,10.0.0.12,00:1A:C2:7B:00:12,2023-03-12T09:46:38Z",
                "D-1003,10.0.0.13,00:1A:C2:7B:00:13,2023-03-12T09:44:59Z",
                "D-1004,10.0.0.14,00:1A:C2:7B:00:14,2023-03-12T09:47:15Z",
                "D-1005,10.0.0.15,00:1A:C2:7B:00:15,2023-03-12T09:48:01Z",
            ],
        ),
    ],
)
def test_csv_files_exist_and_match_expected_content(csv_file, expected_lines):
    assert os.path.isfile(csv_file), f"Required file '{csv_file}' is missing."

    with open(csv_file, "r", encoding="utf-8") as fh:
        actual_lines = [ln.rstrip("\n\r") for ln in fh]

    assert (
        actual_lines == expected_lines
    ), f"Content mismatch in '{csv_file}'.\nExpected:\n{expected_lines}\nActual:\n{actual_lines}"