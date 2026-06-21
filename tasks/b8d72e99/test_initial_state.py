# test_initial_state.py
#
# This test-suite validates the **initial** filesystem/OS state that must be
# present _before_ the student performs any actions.  If any of these tests
# fail, the environment is not correctly prepared and the student will be
# unable to obtain the expected result.

import json
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# CONSTANTS ------------------------------------------------------------------
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
APP_DIR = HOME / "sample_app"
LOG_DIR = APP_DIR / "logs"
STATUS_FILE = APP_DIR / "status.json"
LOG_FILE = LOG_DIR / "app.log"


# ---------------------------------------------------------------------------
# HELPERS --------------------------------------------------------------------
# ---------------------------------------------------------------------------

def read_status_json():
    try:
        with STATUS_FILE.open(encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:  # pragma: no cover  (explicit message elsewhere)
        pytest.fail(f"Required file missing: {STATUS_FILE}", pytrace=False)
    except json.JSONDecodeError as exc:  # pragma: no cover
        pytest.fail(f"{STATUS_FILE} is not valid JSON: {exc}", pytrace=False)


def read_log_lines():
    try:
        return LOG_FILE.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:  # pragma: no cover  (explicit message elsewhere)
        pytest.fail(f"Required file missing: {LOG_FILE}", pytrace=False)


# ---------------------------------------------------------------------------
# TESTS ----------------------------------------------------------------------
# ---------------------------------------------------------------------------

def test_directories_exist():
    """Verify that the expected directories exist."""
    assert APP_DIR.is_dir(), f"Missing application directory: {APP_DIR}"
    assert LOG_DIR.is_dir(), f"Missing logs directory: {LOG_DIR}"


def test_files_exist():
    """Verify that the expected files exist."""
    assert STATUS_FILE.is_file(), f"Missing status file: {STATUS_FILE}"
    assert LOG_FILE.is_file(), f"Missing log file: {LOG_FILE}"


def test_status_json_structure_and_values():
    """
    The JSON status file must contain the exact keys and values
    specified by the ground truth.
    """
    data = read_status_json()

    # Expected structure
    expected_keys = {"pid", "cpu_pct", "mem_pct", "open_ports"}
    assert set(data.keys()) == expected_keys, (
        f"{STATUS_FILE} must contain exactly the keys "
        f"{', '.join(sorted(expected_keys))} (found: {', '.join(sorted(data.keys()))})"
    )

    # Expected values
    assert data["pid"] == 4242, f"Expected pid=4242, found {data['pid']}"
    assert data["cpu_pct"] == 2.3, f"Expected cpu_pct=2.3, found {data['cpu_pct']}"
    assert data["mem_pct"] == 1.1, f"Expected mem_pct=1.1, found {data['mem_pct']}"
    assert data["open_ports"] == [8080, 9090], (
        f"Expected open_ports=[8080, 9090], found {data['open_ports']}"
    )


def test_log_file_content_and_error_lines():
    """
    Validate the contents of the application log:
    * Fewer than 200 total lines
    * Exactly 4 lines containing the substring 'ERROR'
    * Expected distinct ERROR messages appear with correct counts
    """
    lines = read_log_lines()
    total_lines = len(lines)
    assert total_lines < 200, (
        f"{LOG_FILE} should have < 200 lines; found {total_lines}"
    )

    # Inspect last 100 (or fewer) lines
    relevant_lines = lines[-100:]
    error_lines = [ln for ln in relevant_lines if "ERROR" in ln]
    assert len(error_lines) == 4, (
        f"Expected exactly 4 ERROR lines, found {len(error_lines)}"
    )

    # Extract message text after the first whitespace following 'ERROR'
    def extract_message(line: str) -> str:
        # Split once on 'ERROR', then once on the next whitespace
        _, after_error = line.split("ERROR", 1)
        # lstrip to remove the single space that follows 'ERROR'
        return after_error.lstrip()

    messages = [extract_message(ln) for ln in error_lines]

    # Count occurrences preserving order of first appearance
    freq = {}
    for msg in messages:
        freq[msg] = freq.get(msg, 0) + 1

    # The ground-truth expectations
    expected_freq = {
        "Connection timed out to database": 2,
        "Failed to load configuration file": 1,
        "User authentication failed": 1,
    }

    assert freq == expected_freq, (
        "ERROR message frequency mismatch.\n"
        f"Expected: {expected_freq}\nFound:    {freq}"
    )