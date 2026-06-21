# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the operating system / file-system
# BEFORE the student performs any actions for the “performance-tuning engineer” task.
#
# The tests assert that:
#   • The raw log files for serviceA and serviceB exist at the expected absolute paths.
#   • Their contents match the provided ground-truth lines exactly (no extra / missing lines).
#   • No additional *.log files are present under /home/user/app_logs/.
#   • No output artefacts (/home/user/output/perf_summary.log or
#     /home/user/output/anomalies.log) exist yet.
#
# Only stdlib + pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")
APP_LOGS_DIR = HOME / "app_logs"
OUTPUT_DIR = HOME / "output"

SERVICE_A_FILE = APP_LOGS_DIR / "serviceA.log"
SERVICE_B_FILE = APP_LOGS_DIR / "serviceB.log"

# --------------------------------------------------------------------------- #
# Ground-truth contents (exactly as they must appear in the initial files)
# --------------------------------------------------------------------------- #

SERVICE_A_LINES = [
    "2023-07-01T12:00:00Z 120 200",
    "2023-07-01T12:00:01Z 130 200",
    "2023-07-01T12:00:02Z 125 500",
    "2023-07-01T12:00:03Z 140 200",
    "2023-07-01T12:00:04Z 150 200",
    "2023-07-01T12:00:05Z 110 200",
    "2023-07-01T12:00:06Z 115 200",
    "2023-07-01T12:00:07Z 160 503",
    "2023-07-01T12:00:08Z 135 200",
    "2023-07-01T12:00:09Z 145 200",
]

SERVICE_B_LINES = [
    "2023-07-01T12:00:00Z 90 200",
    "2023-07-01T12:00:01Z 95 200",
    "2023-07-01T12:00:02Z 85 200",
    "2023-07-01T12:00:03Z 100 500",
    "2023-07-01T12:00:04Z 92 200",
    "2023-07-01T12:00:05Z 88 200",
    "2023-07-01T12:00:06Z 97 502",
    "2023-07-01T12:00:07Z 89 200",
]

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #


def _read_file_lines(path: Path):
    """
    Return a list of lines (without trailing newlines) from *path*.
    Raises an AssertionError with an informative message if the file is unreadable.
    """
    try:
        return path.read_text().splitlines()
    except FileNotFoundError as exc:
        pytest.fail(f"Expected file not found: {path}", pytrace=False)
    except OSError as exc:
        pytest.fail(f"Could not read file {path}: {exc}", pytrace=False)


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #


def test_app_logs_directory_exists_and_is_directory():
    assert APP_LOGS_DIR.exists(), f"Directory {APP_LOGS_DIR} is missing."
    assert APP_LOGS_DIR.is_dir(), f"{APP_LOGS_DIR} exists but is not a directory."


def test_only_expected_log_files_present():
    """
    /home/user/app_logs/ must contain EXACTLY two files:
        • serviceA.log
        • serviceB.log
    """
    present_logs = sorted(p.name for p in APP_LOGS_DIR.glob("*.log"))
    expected_logs = sorted([SERVICE_A_FILE.name, SERVICE_B_FILE.name])
    assert (
        present_logs == expected_logs
    ), f"Unexpected log files in {APP_LOGS_DIR}. Expected {expected_logs!r} but found {present_logs!r}."


@pytest.mark.parametrize(
    "file_path, expected_lines",
    [
        (SERVICE_A_FILE, SERVICE_A_LINES),
        (SERVICE_B_FILE, SERVICE_B_LINES),
    ],
)
def test_log_file_contents_exact_match(file_path: Path, expected_lines):
    """
    Ensure each log file contains exactly the ground-truth lines (no more, no less).
    """
    actual_lines = _read_file_lines(file_path)
    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {file_path} do not match the expected baseline.\n"
        f"--- Expected ({len(expected_lines)} lines) ---\n"
        + "\n".join(expected_lines)
        + "\n--- Actual ({len(actual_lines)} lines) ---\n"
        + "\n".join(actual_lines)
        + "\n"
    )


def test_output_files_do_not_exist_yet():
    """
    Before the student starts, neither the output directory nor the two
    required artefact files should exist.
    """
    perf_summary = OUTPUT_DIR / "perf_summary.log"
    anomalies = OUTPUT_DIR / "anomalies.log"

    # The directory may or may not exist, but if it does, the files must not be there.
    if OUTPUT_DIR.exists():
        assert not perf_summary.exists(), f"{perf_summary} should NOT exist before the task is run."
        assert not anomalies.exists(), f"{anomalies} should NOT exist before the task is run."
    else:
        # Directory doesn't exist yet – that's acceptable and expected.
        assert True