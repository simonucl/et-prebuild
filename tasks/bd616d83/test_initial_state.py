# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the operating system /
# filesystem before the student begins working on the task.  These tests make
# sure that the required source material is present and correct, and that the
# output artefacts do *not* yet exist.
#
# The environment is expected to look like this *before* the student starts:
#
#   Required to ALREADY exist (and be correct):
#     • /home/user/raw_logs/active_connections.tsv
#     • /home/user/raw_logs/cpu_load.tsv
#
#   Required to NOT YET exist:
#     • /home/user/reports/connection_load_summary.tsv
#     • /home/user/reports/summary_commands.log
#
# If any of these expectations are violated, the tests will fail with a clear
# and helpful message so that the learner can fix the environment before
# proceeding.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
RAW_DIR = HOME / "raw_logs"
REPORTS_DIR = HOME / "reports"

ACTIVE_FILE = RAW_DIR / "active_connections.tsv"
CPU_FILE = RAW_DIR / "cpu_load.tsv"

# Targets (must NOT exist yet)
SUMMARY_FILE = REPORTS_DIR / "connection_load_summary.tsv"
COMMANDS_LOG = REPORTS_DIR / "summary_commands.log"


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def _read_nonempty_lines(path):
    """Return a list of non-empty lines (stripped of trailing newlines)."""
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh if ln.rstrip("\n")]


# --------------------------------------------------------------------------- #
# Tests for the source material (should already exist)
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path, expected_header, expected_col_count, expected_hostnames",
    [
        (
            ACTIVE_FILE,
            ["HOSTNAME", "IP", "PORT", "STATE", "PID"],
            5,
            ["web01", "db01", "cache01"],
        ),
        (
            CPU_FILE,
            ["HOSTNAME", "1min", "5min", "15min"],
            4,
            ["web01", "db01", "cache01"],
        ),
    ],
)
def test_source_files_exist_and_are_correct(
    path, expected_header, expected_col_count, expected_hostnames
):
    # 1) Existence
    assert path.is_file(), f"Required file is missing: {path}"

    # 2) Non-empty
    lines = _read_nonempty_lines(path)
    assert lines, f"File {path} is empty."

    # 3) Header correctness
    header = lines[0].split("\t")
    assert header == expected_header, (
        f"Header mismatch in {path}.\n"
        f"Expected: {expected_header!r}\n"
        f"Found   : {header!r}"
    )

    # 4) Row count (header + 3 data rows)
    assert len(lines) == 4, (
        f"{path} should contain exactly 4 non-empty lines "
        f"(1 header + 3 data), but has {len(lines)}."
    )

    # 5) Column count for each row and hostname order
    hostnames_seen = []
    for idx, line in enumerate(lines[1:], start=2):  # skip header
        cols = line.split("\t")
        assert len(cols) == expected_col_count, (
            f"Line {idx} in {path} has {len(cols)} columns; "
            f"expected {expected_col_count}. Line content: {line!r}"
        )
        hostnames_seen.append(cols[0])

    assert hostnames_seen == expected_hostnames, (
        f"Hostname ordering/content mismatch in {path}.\n"
        f"Expected order: {expected_hostnames}\n"
        f"Found order   : {hostnames_seen}"
    )


# --------------------------------------------------------------------------- #
# Tests ensuring output artefacts do *not* yet exist
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path, description",
    [
        (SUMMARY_FILE, "summary TSV report"),
        (COMMANDS_LOG, "command log"),
    ],
)
def test_target_files_do_not_exist_yet(path, description):
    assert not path.exists(), (
        f"The {description} ({path}) already exists but should NOT be present "
        f"before the student runs the solution commands. Please delete it to "
        f"start with a clean state."
    )


# --------------------------------------------------------------------------- #
# Test that required directories exist (so the student can write into them)
# --------------------------------------------------------------------------- #
def test_required_directories_exist():
    for p in (RAW_DIR, REPORTS_DIR):
        assert p.is_dir(), f"Required directory is missing: {p}"