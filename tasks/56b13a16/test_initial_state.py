# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student’s shell script is executed.  These tests ensure
# that the raw probe file is present and well-formed *and* that none of
# the expected output artefacts have been created yet.
#
# Do **not** modify this file.

import re
from pathlib import Path

import pytest


# ---------------------------------------------------------------------
# Constants that define the expected state
# ---------------------------------------------------------------------

RAW_LOG             = Path("/home/user/data/uptime_checks.log")
REPORTS_DIR         = Path("/home/user/reports")
SUMMARY_TSV         = REPORTS_DIR / "daily_uptime_summary_20240520.tsv"
DOWNTIME_TXT        = REPORTS_DIR / "downtime_20240520.txt"

# Host-level expectations derived from the task description
EXPECTED_COUNTS = {
    "web-1": {"UP": 2, "DOWN": 1},
    "web-2": {"UP": 2, "DOWN": 1},
    "db-1":  {"UP": 3, "DOWN": 0},
}

ISO8601_UTC_REGEX = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)


# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------

def read_log_lines():
    """
    Read the raw log file as UTF-8 and return a list of
    *non-empty* lines (with trailing LF stripped).
    """
    try:
        text = RAW_LOG.read_text(encoding="utf-8")
    except FileNotFoundError:     # pragma: no cover – we want the assert to fail
        pytest.fail(f"Required input file {RAW_LOG} is missing.")

    # Remove the final empty element that splitlines() may give us if the
    # file ends with an LF and nothing else.
    return [ln for ln in text.splitlines() if ln.strip()]


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_raw_log_file_exists_and_is_file():
    assert RAW_LOG.exists(), (
        f"Required file {RAW_LOG} does not exist.  "
        "Make sure the data file is in place before starting."
    )
    assert RAW_LOG.is_file(), f"{RAW_LOG} exists but is not a regular file."


def test_raw_log_line_structure_and_counts():
    lines = read_log_lines()

    # According to the spec there should be 9 probe lines: 3 per host.
    expected_line_count = sum(
        (d["UP"] + d["DOWN"]) for d in EXPECTED_COUNTS.values()
    )
    assert len(lines) == expected_line_count, (
        f"{RAW_LOG} should contain {expected_line_count} non-empty lines "
        f"(one per probe), found {len(lines)}."
    )

    # Parse lines and tally counts
    tally = {host: {"UP": 0, "DOWN": 0} for host in EXPECTED_COUNTS}

    for idx, line in enumerate(lines, start=1):
        parts = line.split()
        assert len(parts) == 3, (
            f"Line {idx} of {RAW_LOG} should have 3 fields "
            f"(TIMESTAMP HOSTNAME RESULT); got {len(parts)} fields: {line!r}"
        )

        ts, host, result = parts

        # Timestamp format check
        assert ISO8601_UTC_REGEX.match(ts), (
            f"Line {idx}: timestamp {ts!r} is not a valid ISO-8601 UTC string "
            f"(expected YYYY-MM-DDThh:mm:ssZ)."
        )

        # Host validity
        assert host in EXPECTED_COUNTS, (
            f"Line {idx}: unexpected host {host!r}. Expected exactly the hosts "
            f"{sorted(EXPECTED_COUNTS)}."
        )

        # Result validity
        assert result in ("UP", "DOWN"), (
            f"Line {idx}: result field must be literally 'UP' or 'DOWN', "
            f"got {result!r}."
        )

        tally[host][result] += 1

    # Final per-host count validation
    for host, expected in EXPECTED_COUNTS.items():
        for state in ("UP", "DOWN"):
            assert tally[host][state] == expected[state], (
                f"Host {host}: expected {expected[state]} {state} record(s) "
                f"but found {tally[host][state]}."
            )


def test_output_reports_do_not_exist_yet():
    """
    Before running the student’s solution, NONE of the required output
    artefacts should be present.  Their presence would indicate that the
    environment is dirty or that a previous run polluted the workspace.
    """
    if REPORTS_DIR.exists():
        # The directory itself is allowed to pre-exist, but the *files*
        # must not be there yet.
        assert not SUMMARY_TSV.exists(), (
            f"Output file {SUMMARY_TSV} already exists but the task has not "
            "been executed yet.  Remove it before running the assessment."
        )
        assert not DOWNTIME_TXT.exists(), (
            f"Output file {DOWNTIME_TXT} already exists but the task has not "
            "been executed yet.  Remove it before running the assessment."
        )
    else:
        # If the directory does not exist that's also OK.
        assert not SUMMARY_TSV.exists(), (
            f"Unexpected file {SUMMARY_TSV} found even though its "
            f"parent directory {REPORTS_DIR} is absent."
        )
        assert not DOWNTIME_TXT.exists(), (
            f"Unexpected file {DOWNTIME_TXT} found even though its "
            f"parent directory {REPORTS_DIR} is absent."
        )