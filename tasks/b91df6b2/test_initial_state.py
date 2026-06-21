# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem / OS state
# required for the “policy-as-code performance benchmark” exercise is
# present and correct *before* the student starts writing any solution.
#
# ONLY prerequisite artefacts (the things that are guaranteed to be in
# the starting repository) are tested here; we deliberately avoid
# asserting on the output files / directories that the student will
# create later on.

import os
import stat
import re
import pytest
from pathlib import Path

# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

BASE_DIR = Path("/home/user/policy_tests")
SCRIPTS_DIR = BASE_DIR / "scripts"
COMPUTE_SH = SCRIPTS_DIR / "compute.sh"
POLICY_CONF = BASE_DIR / "policy.conf"

# Regular expression for KEY=INTEGER lines (allow surrounding whitespace)
KEY_VALUE_RE = re.compile(r"^\s*([A-Z0-9_]+)\s*=\s*([0-9]+)\s*$")


# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------

def test_base_directory_exists():
    """The root directory /home/user/policy_tests must exist."""
    assert BASE_DIR.is_dir(), (
        f"Required directory {BASE_DIR} is missing. "
        "The starting repository appears to be incomplete."
    )


def test_scripts_directory_exists():
    """The scripts sub-directory must be present."""
    assert SCRIPTS_DIR.is_dir(), (
        f"Required directory {SCRIPTS_DIR} is missing. "
        "Expected to find the shell utility here."
    )


def test_compute_script_exists_and_is_executable():
    """
    compute.sh must exist, be a regular file, and have the executable bit
    set for the current user.
    """
    assert COMPUTE_SH.is_file(), (
        f"Expected file {COMPUTE_SH} is missing. "
        "This shell utility is the subject of the benchmark."
    )

    mode = COMPUTE_SH.stat().st_mode
    assert mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH), (
        f"File {COMPUTE_SH} exists but is not marked as executable."
    )


def test_policy_conf_exists_and_has_required_keys():
    """
    policy.conf must exist and contain at least the two required integer
    threshold keys:
        MAX_RUNTIME_MS
        MAX_MEMORY_KB
    """
    assert POLICY_CONF.is_file(), (
        f"Required policy file {POLICY_CONF} is missing."
    )

    # Read and parse the file
    parsed = {}
    with POLICY_CONF.open("r", encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            line = line.strip()
            if not line or line.startswith("#"):
                # Blank line or comment — skip
                continue

            m = KEY_VALUE_RE.match(line)
            assert m, (
                f"Malformed line in {POLICY_CONF} (line {line_no!s}): "
                f"'{line}'. Expected KEY=INTEGER format."
            )
            key, value_str = m.groups()
            try:
                value_int = int(value_str)
            except ValueError:
                pytest.fail(
                    f"Non-integer value in {POLICY_CONF} (line {line_no!s})."
                )
            parsed[key] = value_int

    # Check that the required keys are present and positive integers
    for required_key in ("MAX_RUNTIME_MS", "MAX_MEMORY_KB"):
        assert required_key in parsed, (
            f"{POLICY_CONF} is missing the required key '{required_key}'."
        )
        assert parsed[required_key] > 0, (
            f"{required_key} in {POLICY_CONF} must be a positive integer."
        )