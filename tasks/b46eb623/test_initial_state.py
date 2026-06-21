# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state that must exist *before* the student begins the lab.
#
# 1. /home/user/incident_logs/auth.log must already exist and be readable.
# 2. The log must contain at least one “Failed password” line so that the
#    student has data to process.
# 3. The target output directory (/home/user/analysis) and the two
#    deliverable files must *not* exist yet – the student has to create them.
# 4. Standard text-processing tools awk and sed must be available in $PATH.
#
# Only Python’s standard library and pytest are used.

import os
import re
import shutil
from pathlib import Path

import pytest

HOME = Path("/home/user")
LOG_DIR = HOME / "incident_logs"
AUTH_LOG = LOG_DIR / "auth.log"

ANALYSIS_DIR = HOME / "analysis"
FAILED_REPORT = ANALYSIS_DIR / "failed_login_report.csv"
SANITIZED_LOG = ANALYSIS_DIR / "sanitized_failed.log"


@pytest.mark.describe("Initial authentication log must be in place")
def test_auth_log_exists_and_readable():
    assert AUTH_LOG.exists(), (
        f"Required log file missing: {AUTH_LOG}. "
        "The lab cannot proceed without it."
    )
    assert AUTH_LOG.is_file(), f"{AUTH_LOG} exists but is not a regular file."
    try:
        contents = AUTH_LOG.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {AUTH_LOG}: {exc}")

    # Basic sanity check: at least one ‘Failed password’ entry should exist
    failed_lines = [
        line for line in contents.splitlines() if "Failed password" in line
    ]
    assert failed_lines, (
        f"{AUTH_LOG} must contain at least one line with the text "
        "'Failed password' so the student has data to work on."
    )

    # Each failed line should contain an IPv4 address and a port number.
    ipv4_regex = re.compile(
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    )
    port_regex = re.compile(r"\bport\s+\d+\b", re.IGNORECASE)

    for idx, line in enumerate(failed_lines, start=1):
        assert ipv4_regex.search(line), (
            f"Line {idx} that contains 'Failed password' does not have an "
            f"IPv4 address: {line}"
        )
        assert port_regex.search(line), (
            f"Line {idx} that contains 'Failed password' does not have a "
            f"TCP port number after the word 'port': {line}"
        )


@pytest.mark.describe("Output directory and files must not yet exist")
def test_analysis_directory_absent():
    assert not ANALYSIS_DIR.exists(), (
        f"The directory {ANALYSIS_DIR} should NOT exist before the student "
        "runs their solution.  It will be created by their script."
    )


def test_output_files_absent():
    for path in (FAILED_REPORT, SANITIZED_LOG):
        assert not path.exists(), (
            f"The file {path} should not exist yet. "
            "It will be created by the student's commands."
        )


@pytest.mark.describe("Required command-line tools must be available")
def test_required_tools_present():
    for tool in ("awk", "sed"):
        tool_path = shutil.which(tool)
        assert tool_path, (
            f"The command-line tool '{tool}' is required for this exercise "
            "but was not found in the system PATH."
        )