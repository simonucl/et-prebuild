# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the student runs any commands.  It intentionally does NOT
# look for the eventual output file (`high_temp_errors.log`) because the
# student has not created it yet.
#
# What is verified:
#   1. The logs directory exists at /home/user/iot_deploy/logs and has the
#      expected permissions.
#   2. The sensor log exists at the exact path
#      /home/user/iot_deploy/logs/sensor.log.
#   3. The file permissions for sensor.log are correct.
#   4. The contents of sensor.log match the specification **exactly**
#      (byte-for-byte), including line order and trailing newline.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest

LOG_DIR = "/home/user/iot_deploy/logs"
SENSOR_LOG = os.path.join(LOG_DIR, "sensor.log")

EXPECTED_SENSOR_LINES = [
    "2023-07-01T10:00:00Z INFO device123 TEMP=75.2 HUM=40\n",
    "2023-07-01T10:05:00Z ERROR device123 TEMP=82.5 HUM=42\n",
    "2023-07-01T10:10:00Z WARN device456 TEMP=60.1 HUM=50\n",
    "2023-07-01T10:15:00Z ERROR device789 TEMP=90.0 HUM=35\n",
    "2023-07-01T10:20:00Z INFO device123 TEMP=78.3 HUM=45\n",
    "2023-07-01T10:25:00Z ERROR device456 TEMP=87.4 HUM=47\n",
    "2023-07-01T10:30:00Z INFO device789 TEMP=72.0 HUM=38\n",
]

EXPECTED_DIR_MODE = 0o755
EXPECTED_FILE_MODE = 0o644


def _mode_bits(path):
    """Return the permission bits of a file/dir (e.g. 0o755)."""
    return stat.S_IMODE(os.stat(path).st_mode)


@pytest.mark.describe("Initial filesystem layout")
class TestInitialLayout:
    def test_log_directory_exists(self):
        assert os.path.exists(LOG_DIR), (
            f"Required directory {LOG_DIR!r} is missing."
        )
        assert os.path.isdir(LOG_DIR), (
            f"{LOG_DIR!r} exists but is not a directory."
        )
        mode = _mode_bits(LOG_DIR)
        assert mode == EXPECTED_DIR_MODE, (
            f"Directory {LOG_DIR!r} must have permissions "
            f"{oct(EXPECTED_DIR_MODE)}, but has {oct(mode)} instead."
        )

    def test_sensor_log_file_exists(self):
        assert os.path.exists(SENSOR_LOG), (
            f"Required file {SENSOR_LOG!r} is missing."
        )
        assert os.path.isfile(SENSOR_LOG), (
            f"{SENSOR_LOG!r} exists but is not a regular file."
        )
        mode = _mode_bits(SENSOR_LOG)
        assert mode == EXPECTED_FILE_MODE, (
            f"File {SENSOR_LOG!r} must have permissions "
            f"{oct(EXPECTED_FILE_MODE)}, but has {oct(mode)} instead."
        )

    def test_sensor_log_contents_exact(self):
        # Read the entire file in binary first to make sure the last byte is LF.
        with open(SENSOR_LOG, "rb") as bf:
            content = bf.read()
            assert content.endswith(b"\n"), (
                f"{SENSOR_LOG!r} must end with exactly one LF (\\n) "
                "but does not."
            )

        # Now read in text mode with universal newlines disabled so we see raw '\n'
        with open(SENSOR_LOG, "r", newline="") as tf:
            lines = tf.readlines()

        assert lines == EXPECTED_SENSOR_LINES, (
            f"Contents of {SENSOR_LOG!r} do not match the expected "
            "specification.\n"
            "Expected lines:\n"
            + "".join(EXPECTED_SENSOR_LINES)
            + "\nActual lines:\n"
            + "".join(lines)
        )