# test_initial_state.py
#
# This test-suite validates that the *initial* container file-system is
# correctly populated with the three micro-service log files that the
# student will later process.  The tests purposefully avoid looking for
# any **output** artefacts (reports/, archive/, tarballs, etc.) because
# those should not exist yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")
BASE_DIR = HOME / "microservices"
LOG_DIR = BASE_DIR / "logs"

# ----------------------------------------------------------------------
# Expected directory structure
# ----------------------------------------------------------------------
EXPECTED_DIRECTORIES = [
    BASE_DIR,
    LOG_DIR,
]

# ----------------------------------------------------------------------
# Expected file contents (each list element is one line *without* the \n)
# ----------------------------------------------------------------------
EXPECTED_LOG_CONTENTS = {
    "serviceA.log": [
        "2023-09-14 10:15:32 INFO Starting service",
        "2023-09-14 10:17:02 ERROR Failed to connect to DB",
        "2023-09-14 11:05:12 WARNING Low memory",
        "2023-09-15 09:45:00 INFO Health check passed",
        "2023-09-15 12:08:45 ERROR Timeout while processing request",
        "2023-09-16 13:00:00 INFO Shutdown signal received",
    ],
    "serviceB.log": [
        "2023-09-13 08:00:00 INFO Starting service",
        "2023-09-13 08:30:21 WARNING Cache miss",
        "2023-09-14 09:00:02 ERROR Unhandled exception",
        "2023-09-15 10:05:05 ERROR Null pointer",
        "2023-09-16 11:11:11 WARNING High latency",
        "2023-09-16 12:00:00 INFO Rolling update completed",
    ],
    "serviceC.log": [
        "2023-09-14 14:22:10 INFO Init",
        "2023-09-14 14:23:00 WARNING Deprecated API",
        "2023-09-15 16:45:30 ERROR Disk full",
        "2023-09-15 18:00:00 ERROR Permission denied",
        "2023-09-16 19:30:30 WARNING Configuration reload",
        "2023-09-16 20:00:00 INFO Done",
    ],
}

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def read_file_lines(path: Path):
    """
    Return a list of lines *without* trailing newline characters.
    """
    return path.read_text(encoding="utf-8").splitlines()


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
@pytest.mark.parametrize("directory", EXPECTED_DIRECTORIES)
def test_required_directories_exist(directory: Path):
    assert directory.exists() and directory.is_dir(), (
        f"Required directory missing: {directory}"
    )


def test_no_extra_log_files_present():
    """
    Ensure that the logs/ directory contains exactly the three expected
    *.log files, nothing more and nothing less.
    """
    found_logs = {p.name for p in LOG_DIR.glob("*.log")}
    expected_logs = set(EXPECTED_LOG_CONTENTS.keys())
    missing = expected_logs - found_logs
    extra = found_logs - expected_logs

    msg_parts = []
    if missing:
        msg_parts.append(f"Missing log files: {', '.join(sorted(missing))}")
    if extra:
        msg_parts.append(f"Unexpected extra log files: {', '.join(sorted(extra))}")

    assert not msg_parts, "; ".join(msg_parts)


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_LOG_CONTENTS.items())
def test_log_file_content_and_formatting(filename, expected_lines):
    """
    Validate that each individual log file exists, contains exactly the
    expected lines, and uses LF line endings (no CRLF).
    """
    path = LOG_DIR / filename

    # 1) File existence check
    assert path.exists() and path.is_file(), f"Expected log file missing: {path}"

    # 2) CRLF sanity check (read raw bytes to look for carriage returns)
    raw = path.read_bytes()
    assert b"\r" not in raw, (
        f"File {filename} contains CRLF line endings; only LF is allowed."
    )

    # 3) Content check (line-by-line, ignoring final newline char)
    actual_lines = read_file_lines(path)
    assert actual_lines == expected_lines, (
        f"Contents of {filename} do not match the expected initial state.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(expected_lines)
        + "\n\nActual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )