# test_initial_state.py
#
# Pytest suite that validates the operating-system / file-system state
# **before** the student begins working on the exercise.
#
# Rules enforced:
#   • Only stdlib + pytest are used.
#   • We verify the presence and exact contents of the *input* file only.
#   • We do NOT check for the presence (or absence) of any output files
#     or directories so as not to violate the grading contract.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

SENSOR_FILE = Path("/home/user/data/edge/sensor_raw.csv")

EXPECTED_SENSOR_CONTENT = (
    "timestamp,device_id,tempC,humidity,pressurePa\n"
    "2023-06-15T12:00:00Z,node-01,35.1,45,101325\n"
    "2023-06-15T12:01:00Z,node-01,35.3,44,101327\n"
    "2023-06-15T12:02:00Z,node-02,30.0,50,101300\n"
    "2023-06-15T12:03:00Z,node-03,40.2,38,101400\n"
)

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _read_file(path: Path) -> str:
    """
    Read a file as UTF-8 text and return its full contents.

    A dedicated helper is used so that we can emit a clear error if the
    read unexpectedly fails (e.g., due to permissions or encoding issues).
    """
    try:
        with path.open("r", encoding="utf-8") as fp:
            return fp.read()
    except FileNotFoundError:
        pytest.fail(f"Required file not found: {path}")
    except PermissionError:
        pytest.fail(f"Permission denied when reading: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unexpected error when reading {path}: {exc}")


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_sensor_file_exists_and_is_regular():
    """
    The raw sensor CSV must exist **and** be a regular file.
    """
    assert SENSOR_FILE.exists(), (
        "The required input file does not exist at the expected path:\n"
        f"  {SENSOR_FILE}"
    )
    assert SENSOR_FILE.is_file(), (
        "Expected a regular file at the following path, but something else "
        "(e.g., directory, symlink) was found:\n"
        f"  {SENSOR_FILE}"
    )


def test_sensor_file_contents_exact_match():
    """
    The sensor_raw.csv file must contain the exact 5 lines provided in the
    task description—no more, no less, and no extra whitespace.
    """
    actual = _read_file(SENSOR_FILE)
    assert actual == EXPECTED_SENSOR_CONTENT, (
        "The contents of /home/user/data/edge/sensor_raw.csv do NOT match "
        "the expected initial state.\n\n"
        "=== Expected ===\n"
        f"{EXPECTED_SENSOR_CONTENT!r}\n"
        "=== Actual ===\n"
        f"{actual!r}\n"
        "Please ensure the file has exactly the required 5 lines with no "
        "additional trailing newline or whitespace."
    )