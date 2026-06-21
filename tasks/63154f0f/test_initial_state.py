# test_initial_state.py
#
# This pytest suite validates the initial filesystem state **before**
# the student performs any transformations.  It asserts the presence
# and exact content of the three expected log files under
# /home/user/server_logs/.  It deliberately makes **no reference** to
# any output artefacts or directories.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
LOG_DIR = HOME / "server_logs"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

EXPECTED_FILES = {
    "serverA.log": [
        "2024-07-20 08:11:54 INFO Boot sequence initiated",
        "2024-07-20 08:12:13 ERROR Disk sda IO failure",
        "2024-07-20 08:12:15 ERROR Disk sda IO failure resolved",
        "2024-07-20 08:13:00 INFO Service started",
    ],
    "serverB.log": [
        "2024-07-20 09:00:00 INFO CRON daily job started",
        "2024-07-20 09:00:02 WARN Low entropy",
        "2024-07-20 09:00:24 ERROR Backup failed: remote host unreachable",
        "2024-07-20 09:00:30 INFO CRON daily job finished",
    ],
    "serverC.log": [
        "2024-07-20 10:42:11 INFO Healthcheck OK",
        "2024-07-20 10:45:32 INFO Healthcheck OK",
    ],
}


def read_file_lines(path: pathlib.Path):
    """
    Read a text file using UTF-8, return its lines **without** the trailing
    newline characters.  This makes it easier to compare to the expected list.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh.readlines()]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_log_directory_exists_and_is_directory():
    assert LOG_DIR.exists(), (
        f"Required directory {LOG_DIR} is missing. "
        "It must contain the initial log files."
    )
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


def test_expected_log_files_exist():
    for filename in EXPECTED_FILES:
        fpath = LOG_DIR / filename
        assert fpath.exists(), f"Expected log file {fpath} is missing."
        assert fpath.is_file(), f"{fpath} exists but is not a regular file."


def test_no_unexpected_log_files_present():
    actual_logs = sorted(p.name for p in LOG_DIR.glob("*.log"))
    expected_logs = sorted(EXPECTED_FILES.keys())
    assert actual_logs == expected_logs, (
        "The set of *.log files in the log directory does not match the "
        "expected list.\n"
        f"Expected: {expected_logs}\n"
        f"Found   : {actual_logs}"
    )


@pytest.mark.parametrize("filename, expected_lines", EXPECTED_FILES.items())
def test_each_log_file_has_exact_expected_content(filename, expected_lines):
    """
    Verify that every expected file matches the reference content exactly,
    line by line.
    """
    fpath = LOG_DIR / filename
    actual_lines = read_file_lines(fpath)

    # Helpful diff output on failure.
    assert actual_lines == expected_lines, (
        f"Contents of {fpath} differ from the expected reference.\n"
        "If these files were modified, reset them before running the task."
    )


def test_all_log_files_terminate_with_newline():
    """
    Enforce that each log file ends with a Unix newline (\\n).  This ensures
    that subsequent line-oriented tooling behaves consistently.
    """
    for filename in EXPECTED_FILES:
        fpath = LOG_DIR / filename
        with fpath.open("rb") as fh:
            fh.seek(-1, 2)  # Jump to the last byte
            last_byte = fh.read(1)
        assert last_byte == b"\n", (
            f"{fpath} does not end with a Unix newline (\\n). "
            "Please ensure the file terminates with exactly one newline."
        )