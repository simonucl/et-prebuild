# test_initial_state.py
#
# Pytest suite to validate the initial operating-system / filesystem state
# BEFORE the learner begins the exercise.
#
# The tests verify that the directory /home/user/perf_logs/ exists, contains
# exactly the three expected “.log” files, and that each file’s textual
# content matches the specification in the assignment description.
#
# No assertions are made about any output paths (e.g. /home/user/backups/)
# because those are the artefacts the learner is expected to create later.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

PERF_LOG_DIR = Path("/home/user/perf_logs")

EXPECTED_FILES = {
    "cpu_profile.log": [
        "time,usage",
        "0,12",
        "1,18",
        "2,17",
    ],
    "memory_profile.log": [
        "time,usage",
        "0,153600",
        "1,158720",
        "2,162304",
    ],
    "io_profile.log": [
        "time,bytes",
        "0,4096",
        "1,8192",
        "2,6144",
    ],
}


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------


def read_file_lines(path: Path) -> list[str]:
    """
    Read ``path`` as UTF-8 text and return a list of its lines **exactly** as
    present in the file *without stripping trailing newline characters*.

    The comparison logic later uses ``splitlines()`` (which discards the
    newline characters) to remain agnostic to whether the final line ends in
    “\n”.  This way we accept both POSIX-style files (newline at EOF) and the
    rare case where the very last line lacks it, while still enforcing full
    textual fidelity of every other line.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{path} is not valid UTF-8 text: {exc}")  # noqa: PT012

    return text.splitlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_perf_log_dir_exists_and_is_dir():
    """The directory /home/user/perf_logs/ must exist and be a directory."""
    assert PERF_LOG_DIR.exists(), (
        f"Expected directory {PERF_LOG_DIR} does not exist. "
        "Ensure that the raw profiling logs have been deposited in place."
    )
    assert PERF_LOG_DIR.is_dir(), (
        f"{PERF_LOG_DIR} exists but is not a directory. "
        "It must be a directory that contains the raw '.log' files."
    )


def test_perf_log_dir_contains_only_expected_files():
    """
    /home/user/perf_logs/ must contain **exactly** the three expected “.log”
    files and nothing else (no sub-directories, no extra files).
    """
    actual_entries = sorted(PERF_LOG_DIR.iterdir())
    actual_files = [p.name for p in actual_entries if p.is_file()]
    unexpected_dirs = [p for p in actual_entries if p.is_dir()]

    # Check for unexpected directories first — this is an immediate failure.
    assert not unexpected_dirs, (
        f"The directory {PERF_LOG_DIR} should not contain sub-directories, "
        f"but found: {', '.join(str(d) for d in unexpected_dirs)}"
    )

    expected_files_sorted = sorted(EXPECTED_FILES.keys())
    assert sorted(actual_files) == expected_files_sorted, (
        "Mismatch between expected and actual files inside "
        f"{PERF_LOG_DIR}.\n"
        f"Expected: {expected_files_sorted}\n"
        f"Found   : {sorted(actual_files)}"
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_FILES.items())
def test_each_log_file_content_exact(filename, expected_lines):
    """
    Verify that every expected “.log” file contains exactly the prescribed
    lines, in order, byte-for-byte (apart from a permissible missing newline
    on the very last line).
    """
    file_path = PERF_LOG_DIR / filename
    assert file_path.exists(), f"Missing expected file: {file_path}"
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    actual_lines = read_file_lines(file_path)
    assert actual_lines == expected_lines, (
        f"Contents of {file_path} do not match the specification.\n"
        f"Expected lines:\n{expected_lines}\n\n"
        f"Actual lines:\n{actual_lines}"
    )