# test_initial_state.py
"""
Pytest suite that validates the *initial* state of the on-premise ETL
workspace **before** the student performs any fixes.

The checks purposefully assert that the system is still in the
broken state described in the task, so that the follow-up tests for
the final state can later detect the student’s corrections.
"""

from pathlib import Path
import pytest

# Base path used throughout the tests
BASE_DIR = Path("/home/user/etl")

# Helper paths referenced by several tests
INPUT_DIR  = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
CONFIG_DIR = BASE_DIR / "config"
LOGS_DIR   = BASE_DIR / "logs"

JOB_CONFIG          = CONFIG_DIR / "job_config.yaml"
HISTORICAL_LOG      = LOGS_DIR / "etl_2023-01-01.log"
SUCCESS_MARKER_FILE = OUTPUT_DIR / "SUCCESS_2023-01-02.ok"
DEBUG_SESSION_LOG   = LOGS_DIR / "debug_session.log"


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (BASE_DIR,           "top-level /home/user/etl directory"),
        (INPUT_DIR,          "input directory"),
        (OUTPUT_DIR,         "output directory"),
        (CONFIG_DIR,         "config directory"),
        (LOGS_DIR,           "logs directory"),
    ],
)
def test_directories_exist(path_obj: Path, description: str):
    """Verify that the required directory structure already exists."""
    assert path_obj.exists(), f"Missing {description}: expected directory at {path_obj}"
    assert path_obj.is_dir(), f"{description} at {path_obj} exists but is not a directory"


@pytest.mark.parametrize(
    "file_path, description",
    [
        (INPUT_DIR / "input_data.csv", "sample input CSV"),
        (JOB_CONFIG,                  "job configuration YAML"),
        (HISTORICAL_LOG,              "historical ETL log"),
    ],
)
def test_required_files_exist(file_path: Path, description: str):
    """Ensure that the essential seed files are present."""
    assert file_path.exists(), f"Missing {description}: expected file at {file_path}"
    assert file_path.is_file(), f"{description} at {file_path} exists but is not a regular file"


def test_job_config_has_incorrect_delimiter_setting():
    """
    The initial YAML configuration is *incorrect* on purpose.
    It must still contain 'delimiter: \";\"' and must NOT yet
    contain the corrected line with a comma.
    """
    content = JOB_CONFIG.read_text(encoding="utf-8").splitlines()

    has_wrong_line = any(line.strip() == 'delimiter: ";"' for line in content)
    has_fixed_line = any(line.strip() == 'delimiter: ","' for line in content)

    assert has_wrong_line, (
        f"{JOB_CONFIG} should initially contain the faulty line "
        "'delimiter: \";\"' but it was not found."
    )
    assert not has_fixed_line, (
        f"{JOB_CONFIG} already contains the fixed line "
        "'delimiter: \",\"' — the student has apparently modified the "
        "initial state prematurely."
    )


def test_historical_log_mentions_delimiter_error():
    """
    The provided historical log must mention the known delimiter
    mismatch error so the student can diagnose the issue.
    """
    log_text = HISTORICAL_LOG.read_text(encoding="utf-8")
    expected_snippet = "DelimiterMismatchError: expected ';' but found ',' on line 1"
    assert expected_snippet in log_text, (
        f"{HISTORICAL_LOG} does not contain the expected error message:\n"
        f"    {expected_snippet}"
    )


def test_output_directory_is_empty_and_no_success_marker():
    """
    At the very beginning the output directory must be empty and the
    success marker must not yet exist.
    """
    assert not SUCCESS_MARKER_FILE.exists(), (
        f"Success marker {SUCCESS_MARKER_FILE} already exists; "
        "the job appears to have been run before the student starts."
    )

    entries = [p for p in OUTPUT_DIR.iterdir() if p.name != ".gitkeep"]
    assert not entries, (
        f"{OUTPUT_DIR} is expected to be empty, but it contains: "
        + ", ".join(str(p) for p in entries)
    )


def test_debug_session_log_does_not_exist_yet():
    """
    The structured debug session log should not be present until the
    student creates it.
    """
    assert not DEBUG_SESSION_LOG.exists(), (
        f"{DEBUG_SESSION_LOG} already exists; "
        "the debug session should not have been logged yet."
    )