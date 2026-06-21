# test_initial_state.py
#
# Pytest test-suite that validates the **initial** operating-system state
# before the student’s solution runs.  It checks the presence of the raw
# log file and absence of any artefacts the student is expected to create
# later.  All paths are absolute; no third-party libraries are used.

import pathlib
import textwrap

import pytest

HOME = pathlib.Path("/home/user").expanduser()
GATEWAY_DIR = HOME / "iot_gateway"
LOG_DIR = GATEWAY_DIR / "logs"
REPORTS_DIR = GATEWAY_DIR / "reports"
LOG_FILE = LOG_DIR / "device_events.log"
SUMMARY_FILE = REPORTS_DIR / "summary.csv"
ERROR_LOG_FILE = REPORTS_DIR / "error_events.log"

# ---------------------------------------------------------------------------
# Expected initial content of device_events.log (each line must end with '\n')
# ---------------------------------------------------------------------------
EXPECTED_LOG_CONTENT = textwrap.dedent("""\
    2023-10-11T14:00:01Z device-001 DATA_UPLOAD 110 200
    2023-10-11T14:05:23Z device-002 DATA_UPLOAD 95 200
    2023-10-11T14:12:47Z device-001 HEARTBEAT 30 200
    2023-10-11T14:20:11Z device-003 DATA_UPLOAD 150 500
    2023-10-11T14:45:00Z device-002 HEARTBEAT 28 200
    2023-10-11T15:15:42Z device-001 DATA_UPLOAD 130 504
    2023-10-11T15:40:17Z device-003 HEARTBEAT 32 200
    2023-10-11T16:00:00Z device-004 DATA_UPLOAD 200 200
    2023-10-11T16:10:05Z device-004 HEARTBEAT 33 404
    2023-10-11T16:30:21Z device-002 DATA_UPLOAD 97 200
    2023-10-11T16:35:00Z device-001 HEARTBEAT 29 200
    2023-10-11T17:10:45Z device-003 DATA_UPLOAD 160 200
    2023-10-11T17:20:35Z device-005 DATA_UPLOAD 180 502
    2023-10-11T17:35:20Z device-005 HEARTBEAT 31 200
    2023-10-11T17:45:50Z device-002 DATA_UPLOAD 101 503
""").splitlines(keepends=True)

# Ensure every expected line ends with a single '\n'
EXPECTED_LOG_CONTENT = [line if line.endswith("\n") else f"{line}\n"
                        for line in EXPECTED_LOG_CONTENT]


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def read_file_lines(path: pathlib.Path):
    """Read a file in binary mode and return list of decoded lines."""
    data = path.read_bytes()
    # Carriage returns must not be present anywhere in the file.
    if b"\r" in data:
        pytest.fail(f"File {path} contains CR (\\r) characters; expected LF only")
    text = data.decode("utf-8")
    # Guarantee the file ends with exactly one newline (LF).
    if not text.endswith("\n"):
        pytest.fail(f"File {path} must end with a single LF newline")
    return text.splitlines(keepends=True)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    """The base directories must be in place."""
    for d in (HOME, GATEWAY_DIR, LOG_DIR):
        assert d.is_dir(), f"Expected directory {d} to exist"


def test_reports_directory_absent_initially():
    """/reports must NOT exist before the student creates it."""
    assert not REPORTS_DIR.exists(), (
        f"Directory {REPORTS_DIR} should not exist yet; "
        "it will be created by the student's script."
    )


def test_log_file_presence():
    """The raw device_events.log must exist and be a regular file."""
    assert LOG_FILE.is_file(), f"Required log file {LOG_FILE} is missing"


def test_log_file_content_exact_match():
    """Log file must contain exactly the expected 15 lines, in order."""
    lines = read_file_lines(LOG_FILE)

    assert len(lines) == len(EXPECTED_LOG_CONTENT), (
        f"{LOG_FILE} should contain {len(EXPECTED_LOG_CONTENT)} lines "
        f"but has {len(lines)}"
    )

    # Compare line by line to give precise feedback on first mismatch.
    for idx, (got, exp) in enumerate(zip(lines, EXPECTED_LOG_CONTENT), start=1):
        assert got == exp, (
            f"Mismatch on line {idx} of {LOG_FILE}:\n"
            f"  expected: {exp!r}\n"
            f"       got: {got!r}"
        )


def test_output_files_absent_initially():
    """No output artefacts should exist before the solution runs."""
    for f in (SUMMARY_FILE, ERROR_LOG_FILE):
        assert not f.exists(), (
            f"File {f} should not exist yet; it will be produced by the student's code."
        )