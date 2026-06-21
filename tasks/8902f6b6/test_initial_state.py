# test_initial_state.py
#
# This test-suite verifies the *starting* file-system state for the KPI-report
# exercise.  It checks that the required input files exist with the exact
# expected content and that the output artefacts the student is supposed to
# create do *not* yet exist.  All paths are absolute to comply with the grading
# rules.

from pathlib import Path
import pytest

AUTOMATION_DIR = Path("/home/user/automation")
INPUT_DIR = AUTOMATION_DIR / "input"
OUTPUT_DIR = AUTOMATION_DIR / "output"
LOGS_DIR = AUTOMATION_DIR / "logs"

SERVERS_CSV = INPUT_DIR / "servers.csv"
METRICS_CSV = INPUT_DIR / "metrics.csv"
COMBINED_CSV = OUTPUT_DIR / "combined.csv"
LOG_FILE = LOGS_DIR / "column_extraction.log"


@pytest.fixture(scope="module")
def expected_servers_content():
    """Exact, newline-stripped lines expected in servers.csv (pre-task)."""
    return [
        "id,name,ip,location",
        "srv01,alpha,10.0.0.1,us-east",
        "srv02,beta,10.0.0.2,us-west",
        "srv03,gamma,10.0.0.3,eu-central",
    ]


@pytest.fixture(scope="module")
def expected_metrics_content():
    """Exact, newline-stripped lines expected in metrics.csv (pre-task)."""
    return [
        "metric_id,server_id,cpu,mem,disk",
        "m001,srv01,55,68,70",
        "m002,srv02,35,40,50",
        "m003,srv03,60,52,80",
    ]


def test_directory_structure():
    """Validate that /home/user/automation and its input/ folder exist."""
    assert AUTOMATION_DIR.is_dir(), (
        f"Required directory {AUTOMATION_DIR} is missing.  "
        "Create it before proceeding."
    )
    assert INPUT_DIR.is_dir(), (
        f"Required input directory {INPUT_DIR} is missing.  "
        "It must contain the two CSV source files."
    )


def _read_csv_lines(path: Path):
    try:
        with path.open("r", encoding="utf-8") as fh:
            # Strip *one* trailing newline per line for comparison.
            return [line.rstrip("\n") for line in fh.readlines()]
    except FileNotFoundError:
        pytest.fail(f"Expected file {path} is missing.")


def test_servers_csv_present_and_correct(expected_servers_content):
    """servers.csv must exist and match the exact expected content."""
    lines = _read_csv_lines(SERVERS_CSV)
    assert lines == expected_servers_content, (
        f"{SERVERS_CSV} content does not match the expected template.\n"
        "If this file was modified, restore the original content."
    )


def test_metrics_csv_present_and_correct(expected_metrics_content):
    """metrics.csv must exist and match the exact expected content."""
    lines = _read_csv_lines(METRICS_CSV)
    assert lines == expected_metrics_content, (
        f"{METRICS_CSV} content does not match the expected template.\n"
        "If this file was modified, restore the original content."
    )


def test_output_files_absent_initially():
    """
    The student is supposed to create output/combined.csv and
    logs/column_extraction.log.  Neither should exist *before* the task is
    attempted.
    """
    # output/ and logs/ directories may or may not exist yet.  We only insist
    # that the target files do not exist so the exercise starts cleanly.
    assert not COMBINED_CSV.exists(), (
        f"File {COMBINED_CSV} already exists.  "
        "Remove it so the exercise starts from a clean slate."
    )
    assert not LOG_FILE.exists(), (
        f"File {LOG_FILE} already exists.  "
        "Remove it so the exercise starts from a clean slate."
    )