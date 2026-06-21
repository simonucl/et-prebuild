# test_initial_state.py
#
# Pytest suite ensuring the machine is in a pristine state
# BEFORE the student carries out the “configuration-manager” exercise.
#
# These tests deliberately assert that *nothing* created by the target
# assignment is present yet.  They also confirm that the only external
# tool we rely on (curl) is available.
#
# If any of these assertions fail, the student must first clean up the
# machine so that their automated solution starts from a known baseline.

import os
import subprocess
from pathlib import Path

# ---------------------------------------------------------------------
# Constants – absolute paths that MUST NOT exist at the outset
# ---------------------------------------------------------------------
HOME = Path("/home/user")
WORKSPACE_DIR = HOME / "config_manager"
CONFIG_JSON = WORKSPACE_DIR / "config.json"
AUDIT_LOG = WORKSPACE_DIR / "audit.log"
RESPONSES_DIR = WORKSPACE_DIR / "responses"
INITIAL_RESP = RESPONSES_DIR / "initial_config.json"
FINAL_RESP = RESPONSES_DIR / "final_config.json"

# ---------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------
def _pretty_path(path: Path) -> str:
    """Return a prettified absolute str path for messages."""
    return str(path.resolve())

# ---------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------
def test_workspace_directory_absent():
    """
    The workspace directory /home/user/config_manager must NOT exist yet.
    The entire directory tree is supposed to be created by the student’s
    script, so its prior existence indicates a stale or dirty environment.
    """
    assert not WORKSPACE_DIR.exists(), (
        f"Workspace directory {_pretty_path(WORKSPACE_DIR)} already exists; "
        "start with a clean slate."
    )

def test_config_file_absent():
    """
    The target configuration file must not exist before the exercise starts.
    """
    assert not CONFIG_JSON.exists(), (
        f"Found unexpected file {_pretty_path(CONFIG_JSON)}; remove it first."
    )

def test_audit_log_absent():
    """
    The audit log must be created by the student’s work; it must not pre-exist.
    """
    assert not AUDIT_LOG.exists(), (
        f"Found unexpected audit log {_pretty_path(AUDIT_LOG)}; remove it first."
    )

def test_responses_directory_absent():
    """
    The responses/ directory is created by the exercise.  It must be absent now.
    """
    assert not RESPONSES_DIR.exists(), (
        f"Found unexpected directory {_pretty_path(RESPONSES_DIR)}; "
        "the environment is not clean."
    )

def test_response_files_absent():
    """
    Neither of the response JSON files may exist at the outset.
    """
    for resp_file in (INITIAL_RESP, FINAL_RESP):
        assert not resp_file.exists(), (
            f"Found unexpected file {_pretty_path(resp_file)}; "
            "remove it before running the exercise."
        )

def test_curl_is_available():
    """
    curl must be available in PATH because the assignment explicitly
    requires using curl with the file:// URI-scheme.
    """
    try:
        result = subprocess.run(
            ["curl", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except FileNotFoundError:
        pytest.fail(
            "curl is not installed or not found in PATH; "
            "it is required for the upcoming exercise."
        )
    else:
        assert "curl" in result.stdout.lower(), (
            "curl command did not execute correctly; "
            "ensure curl is functional."
        )