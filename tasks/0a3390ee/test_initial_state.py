# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any action.  It asserts that the raw log exists in
# the correct location with the exact expected content **and** that the
# output file to be produced by the student is not present yet.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "logs"
RAW_LOG = LOG_DIR / "app.log"
SUMMARY_LOG = LOG_DIR / "login_summary.log"

# ---------------------------------------------------------------------------
# Fixtures & helpers
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def raw_log_lines():
    """
    Read the raw log file and return a list of its lines (without trailing
    newline characters).

    The fixture will fail immediately if the log directory or the file is
    missing so that later tests are not executed against a bad state.
    """
    # 1. Directory must exist
    assert LOG_DIR.is_dir(), (
        f"Required directory {LOG_DIR} is missing. "
        "The initial state must provide this directory."
    )

    # 2. File must exist
    assert RAW_LOG.exists(), (
        f"Required file {RAW_LOG} is missing. "
        "The initial state must include the raw audit log."
    )

    # 3. Read the file
    data = RAW_LOG.read_text(encoding="utf-8")

    # Normalise splitlines so we can make exact assertions line-by-line
    return data.splitlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_raw_log_has_exactly_three_lines(raw_log_lines):
    """The raw log must contain exactly three lines."""
    assert len(raw_log_lines) == 3, (
        f"{RAW_LOG} should contain exactly 3 lines, found {len(raw_log_lines)}."
    )


@pytest.mark.parametrize(
    "expected",
    [
        "2023-07-21 10:33:45,123 [INFO] [user-service] User 'alice' logged in from 10.0.0.12 (session:abc123)",
        "2023-07-21 11:12:07,456 [INFO] [user-service] User 'bob' logged in from 10.0.0.15 (session:def456)",
        "2023-07-21 12:55:22,789 [INFO] [user-service] User 'charlie' logged in from 10.0.0.18 (session:ghi789)",
    ],
)
def test_raw_log_content_matches(expected, raw_log_lines):
    """Each line of the raw log must match the canonical content exactly."""
    assert expected in raw_log_lines, (
        f"The line \n    {expected!r}\n"
        f"was not found in {RAW_LOG}. "
        "Ensure the raw log contains the expected canonical records."
    )


def test_summary_log_absent_initially():
    """
    The derived summary log **must not** exist before the student runs
    their solution.
    """
    assert not SUMMARY_LOG.exists(), (
        f"{SUMMARY_LOG} is present before the student has performed any action. "
        "The initial state must *not* contain this file."
    )