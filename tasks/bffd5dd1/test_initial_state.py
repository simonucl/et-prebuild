# test_initial_state.py
# Pytest suite that validates the operating-system state **before** the student
# performs any action for the “incident triage” exercise.
#
# What we check:
#   • The directory /home/user/incident_triage/ exists.
#   • The sub-directory /home/user/incident_triage/input/ exists.
#   • Exactly three expected *.log files are present in the input directory.
#   • The /home/user/incident_triage/output/ directory does *not* exist yet.
#   • Each *.log file contains the required key/value pairs, with the exact
#     values defined in the task description.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/incident_triage")
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

EXPECTED_FILES = {
    "solver_a.log": {
        "status": "OPTIMAL",
        "iterations": "145",
        "objective": "1234.5678",
        "solve_time_sec": "2.345",
    },
    "solver_b.log": {
        "status": "INFEASIBLE",
        "iterations": "87",
        "objective": "nan",
        "solve_time_sec": "1.230",
    },
    "solver_c.log": {
        "status": "TIME_LIMIT",
        "iterations": "1000",
        "objective": "99999.999",
        "solve_time_sec": "60.000",
    },
}


def test_base_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected directory {BASE_DIR} to exist, but it does not. "
        "Verify the initial directory tree."
    )


def test_input_directory_exists():
    assert INPUT_DIR.is_dir(), (
        f"Expected directory {INPUT_DIR} to exist, but it does not. "
        "The 'input' directory holding the raw log files is missing."
    )


def test_expected_log_files_present_and_no_extras():
    # Collect *.log files in the input directory.
    actual_logs = {p.name for p in INPUT_DIR.glob("*.log")}
    expected_logs = set(EXPECTED_FILES)

    missing = expected_logs - actual_logs
    extras = actual_logs - expected_logs

    assert not missing, (
        "The following expected .log files are missing from the input "
        f"directory {INPUT_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extras, (
        "Unexpected .log files found in the input directory "
        f"{INPUT_DIR}: {', '.join(sorted(extras))}"
    )


@pytest.mark.parametrize("filename,expected_kv", EXPECTED_FILES.items())
def test_each_log_contains_correct_key_values(filename, expected_kv):
    file_path = INPUT_DIR / filename
    assert file_path.is_file(), f"Missing expected log file: {file_path}"

    # Read file once; we don't assume a specific encoding but default 'utf-8' is fine.
    text = file_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # Collect only the lines of the form key=value for the four required keys.
    kv = {}
    for line in lines:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            if key in expected_kv:
                kv[key] = value

    # Check that we captured *all* required keys.
    for key, expected_value in expected_kv.items():
        assert key in kv, (
            f"In {file_path}: expected key '{key}' not found. "
            "Ensure each log line 'key=value' is present."
        )
        assert kv[key] == expected_value, (
            f"In {file_path}: key '{key}' has value '{kv[key]}' "
            f"but expected '{expected_value}'. Verify the file contents."
        )


def test_output_directory_absent():
    assert not OUTPUT_DIR.exists(), (
        f"Directory {OUTPUT_DIR} should NOT exist before the student "
        "runs their solution, but it is present."
    )