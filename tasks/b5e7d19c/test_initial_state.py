# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state **before**
# the student starts working on the “Generate roll-out summary & retry list”
# exercise.  It checks only the pre-existing directory and log file that
# the task description guarantees.  It deliberately does **not** look for
# the two output artefacts that the student will have to create later on.

import os
import stat
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------

DEPLOY_DIR = Path("/home/user/deployments")
LOG_FILE   = DEPLOY_DIR / "updates-2023-06-30.log"

# The exact byte-for-byte contents the log file must have.
_EXPECTED_LOG_CONTENT = (
    "2023-06-30T10:00:00Z node_id=node-a STATUS=SUCCESS version=2.1.0\n"
    "2023-06-30T10:00:02Z node_id=node-b STATUS=FAIL    version=2.1.0\n"
    "2023-06-30T10:00:04Z node_id=node-c STATUS=SUCCESS version=2.1.0\n"
    "2023-06-30T10:00:06Z node_id=node-d STATUS=SUCCESS version=2.1.0\n"
    "2023-06-30T10:00:08Z node_id=node-e STATUS=FAIL    version=2.1.0\n"
    "2023-06-30T10:00:10Z node_id=node-f STATUS=SUCCESS version=2.1.0\n"
    "2023-06-30T10:00:12Z node_id=node-g STATUS=SUCCESS version=2.1.0\n"
)

# Derived ground-truth values that downstream tasks will have to compute.
_EXPECTED_TOTAL_NODES = 7
_EXPECTED_SUCCESS_NODES = {"node-a", "node-c", "node-d", "node-f", "node-g"}
_EXPECTED_FAIL_NODES    = {"node-b", "node-e"}


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _octal_mode(path: Path) -> int:
    """
    Return the permission bits of *path* as an octal integer, e.g. 0o755.
    """
    return stat.S_IMODE(path.stat().st_mode)


def _parse_log_lines(lines):
    """
    Very small parser that extracts node_id → status from the deployment log.
    Returns a dict {<node_id>: <status string>}.
    """
    mapping = {}
    for ln in lines:
        parts = ln.split()
        kv_pairs = dict(p.split("=", 1) for p in parts[1:])  # skip timestamp
        node_id = kv_pairs.get("node_id")
        status  = kv_pairs.get("STATUS")
        if node_id is None or status is None:
            raise ValueError(f"Malformed log line: {ln!r}")
        mapping[node_id] = status
    return mapping


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_deployments_directory_exists_and_permissions():
    assert DEPLOY_DIR.exists(), (
        f"Required directory {DEPLOY_DIR} is missing."
    )
    assert DEPLOY_DIR.is_dir(), (
        f"{DEPLOY_DIR} exists but is not a directory."
    )
    expected_mode = 0o755
    actual_mode   = _octal_mode(DEPLOY_DIR)
    assert actual_mode == expected_mode, (
        f"{DEPLOY_DIR} must have permissions {oct(expected_mode)}, "
        f"but has {oct(actual_mode)}."
    )


def test_log_file_exists_with_exact_content():
    assert LOG_FILE.exists(), f"Required log file {LOG_FILE} is missing."
    assert LOG_FILE.is_file(), f"{LOG_FILE} exists but is not a regular file."

    content = LOG_FILE.read_text(encoding="utf-8")
    assert content == _EXPECTED_LOG_CONTENT, (
        f"Contents of {LOG_FILE} differ from the expected baseline. "
        f"This file must remain unmodified.\n\n"
        "Tip: Run `diff -u` against the expected content shown in the task "
        "description to spot the differences."
    )


def test_log_file_parses_to_expected_node_counts():
    """
    Parse the log to ensure that ground-truth counts match the exercise
    description.  This guards against any hidden alterations to the log.
    """
    lines = _EXPECTED_LOG_CONTENT.rstrip("\n").split("\n")
    mapping = _parse_log_lines(lines)

    # Basic sanity checks
    assert len(mapping) == _EXPECTED_TOTAL_NODES, (
        f"Expected {_EXPECTED_TOTAL_NODES} unique nodes in the log, "
        f"found {len(mapping)}."
    )

    # Split nodes by status
    success_nodes = {n for n, s in mapping.items() if s == "SUCCESS"}
    fail_nodes    = {n for n, s in mapping.items() if s == "FAIL"}

    assert success_nodes == _EXPECTED_SUCCESS_NODES, (
        f"SUCCESS node set mismatch.\n"
        f"Expected: {_EXPECTED_SUCCESS_NODES}\n"
        f"Found   : {success_nodes}"
    )
    assert fail_nodes == _EXPECTED_FAIL_NODES, (
        f"FAIL node set mismatch.\n"
        f"Expected: {_EXPECTED_FAIL_NODES}\n"
        f"Found   : {fail_nodes}"
    )