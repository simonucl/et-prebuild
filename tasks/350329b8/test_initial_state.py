# test_initial_state.py
#
# Pytest suite that asserts the “starting point” of the exercise *before*
# the student executes any command‐line solution.  It validates that the
# shipping container contains exactly the three policy YAML files in
# /home/user/policies/ with the expected contents and that no audit artefacts
# have been created yet.
#
# The tests purposefully **fail fast** with clear, actionable error messages
# if the environment differs from the declared truth-table in the exercise
# description.

import os
import pytest

POLICY_DIR = "/home/user/policies"
AUDIT_DIR = "/home/user/audit"
AUDIT_LOG = os.path.join(AUDIT_DIR, "disabled_policies.log")

EXPECTED_POLICIES = {
    "policy-001.yaml": {
        "id": "policy-001",
        "enabled": "true",   # must exist and be literally "true"
    },
    "policy-002.yaml": {
        "id": "policy-002",
        "enabled": "false",  # must exist and be literally "false"
    },
    "policy-003.yaml": {
        "id": "policy-003",
        "enabled": None,     # key must be absent
    },
}


@pytest.fixture(scope="module")
def policy_files():
    """
    Returns a mapping of filename -> full_path.
    Raises a single assert if the directory is missing.
    """
    assert os.path.isdir(
        POLICY_DIR
    ), f"Required directory {POLICY_DIR!r} is missing."
    files = {
        fname: os.path.join(POLICY_DIR, fname) for fname in os.listdir(POLICY_DIR)
    }
    return files


def test_exact_policy_file_set(policy_files):
    """Assert that the policies directory contains *exactly* the expected files."""
    expected = set(EXPECTED_POLICIES.keys())
    found = set(policy_files.keys())
    assert (
        expected == found
    ), f"{POLICY_DIR} must contain only {sorted(expected)}, but found {sorted(found)}."


@pytest.mark.parametrize("filename,meta", EXPECTED_POLICIES.items())
def test_policy_file_exists_and_contents(policy_files, filename, meta):
    """Validate each YAML file exists and its key fields match the truth table."""
    path = policy_files[filename]
    assert os.path.isfile(path), f"Expected file {path!r} is missing."

    # Read file once; we only need a lightweight key/value grab.
    with open(path, encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]

    # Helper: extract "<key>: <value>" into dict (naïve but sufficient here).
    kv = {}
    for raw in lines:
        # ignore comments & blank lines
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" in stripped:
            k, v = stripped.split(":", 1)
            kv[k.strip()] = v.strip()

    # Validate ID
    expected_id = meta["id"]
    actual_id = kv.get("id")
    assert (
        actual_id == expected_id
    ), f"{path}: expected id: {expected_id!r}, found: {actual_id!r}"

    # Validate enabled flag presence/value as specified.
    expected_enabled = meta["enabled"]
    actual_enabled_present = "enabled" in kv
    if expected_enabled is None:
        assert (
            not actual_enabled_present
        ), f"{path}: 'enabled' key must be absent but is present with value {kv['enabled']!r}"
    else:
        assert actual_enabled_present, f"{path}: missing required 'enabled' key."
        actual_enabled = kv["enabled"]
        assert (
            actual_enabled == expected_enabled
        ), f"{path}: expected enabled: {expected_enabled!r}, found: {actual_enabled!r}"


def test_no_audit_directory_or_log_yet():
    """The audit artefacts should NOT exist before the student runs their command."""
    assert not os.path.exists(
        AUDIT_DIR
    ), f"Unexpected directory {AUDIT_DIR!r} already exists; exercise should start without it."

    assert not os.path.exists(
        AUDIT_LOG
    ), f"Unexpected file {AUDIT_LOG!r} already exists; exercise should start without it."