# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present before the student carries out the task.  It purposefully ignores
# any artefacts that the student is expected to create (e.g. the
# /home/user/analysis_results/ directory and its CSV file).
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants describing the required pre-existing structure and contents
# ---------------------------------------------------------------------------

DATA_DIR = Path("/home/user/data_runs")

EXPECTED_FILES_CONTENT = {
    "run1.log": (
        "[2024-01-01 10:00:00] INFO Starting run\n"
        "[2024-01-01 10:01:00] ERROR Failed to open file\n"
        "[2024-01-01 10:02:00] WARNING Low memory\n"
        "[2024-01-01 10:03:00] ERROR Timeout occurred\n"
        "[2024-01-01 10:04:00] INFO Run finished\n"
    ),
    "run2.log": (
        "[2024-02-01 11:00:00] INFO Starting run\n"
        "[2024-02-01 11:15:00] ERROR Invalid parameter\n"
        "[2024-02-01 11:30:00] INFO Run finished\n"
    ),
    "run3.log": (
        "[2024-03-05 09:00:00] INFO Starting run\n"
        "[2024-03-05 09:05:00] WARNING Disk almost full\n"
        "[2024-03-05 09:10:00] INFO Still running\n"
        "[2024-03-05 09:15:00] ERROR Segmentation fault\n"
        "[2024-03-05 09:20:00] ERROR Failed to allocate memory\n"
        "[2024-03-05 09:25:00] ERROR Unknown exception\n"
        "[2024-03-05 09:30:00] INFO Run finished\n"
    ),
}

# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_data_runs_directory_exists_and_is_directory():
    """Ensure /home/user/data_runs/ exists and is a directory."""
    assert DATA_DIR.exists(), (
        f"Required directory '{DATA_DIR}' does not exist. "
        "Create it and place the log files inside."
    )
    assert DATA_DIR.is_dir(), (
        f"'{DATA_DIR}' exists but is not a directory."
    )


@pytest.mark.parametrize("log_name", sorted(EXPECTED_FILES_CONTENT.keys()))
def test_each_log_file_exists(log_name):
    """Verify that every expected *.log file exists and is a regular file."""
    log_path = DATA_DIR / log_name
    assert log_path.exists(), (
        f"Expected log file '{log_path}' is missing."
    )
    assert log_path.is_file(), (
        f"'{log_path}' exists but is not a regular file."
    )


@pytest.mark.parametrize("log_name,expected_content", EXPECTED_FILES_CONTENT.items())
def test_log_file_contents_exact_match(log_name, expected_content):
    """
    Confirm that the content of each log file matches exactly the
    canonical text—including new-line placement and order.
    """
    log_path = DATA_DIR / log_name
    with log_path.open("r", encoding="utf-8") as fh:
        actual = fh.read()

    # Using == gives a clear diff when pytest is run with -vv
    assert actual == expected_content, (
        f"Contents of '{log_path}' do not match the expected reference text.\n"
        "If you modified the log files, please restore them to their original "
        "state before proceeding."
    )


def test_no_unexpected_files_in_data_runs():
    """
    Sanity-check that there are no unexpected files in /home/user/data_runs/.
    This helps catch typos such as 'run01.log' or stray temporary files.
    """
    present = {p.name for p in DATA_DIR.iterdir() if p.is_file()}
    expected = set(EXPECTED_FILES_CONTENT.keys())
    unexpected = present - expected
    assert not unexpected, (
        "Unexpected file(s) found in /home/user/data_runs/: "
        f"{', '.join(sorted(unexpected))}. "
        "Only run1.log, run2.log and run3.log should be present at this stage."
    )