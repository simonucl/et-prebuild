# test_initial_state.py
"""
Pytest suite that validates the starting filesystem / OS state for the
“IoT gateway diagnostic-bundle” exercise *before* the student performs
any actions.

If any of these tests fail it means the container was not provisioned
correctly **or** the student has already altered the initial state,
both of which would invalidate the grading assumptions.

Only stdlib + pytest are used.
"""

import os
from pathlib import Path

# Constants
HOME_DIR = Path("/home/user")
DEPLOY_DIR = HOME_DIR / "iot_deployment"
DEVICES_TXT = DEPLOY_DIR / "devices.txt"
DIAG_DIR = DEPLOY_DIR / "diagnostics"
SYSTEM_JSON = DIAG_DIR / "system_report.json"
PING_CSV = DIAG_DIR / "ping_summary.csv"

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def read_text(path: Path) -> str:
    """Return text content of path (assumes UTF-8)."""
    return path.read_text(encoding="utf-8")

# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

def test_deployment_directory_exists():
    assert DEPLOY_DIR.exists(), (
        f"Required directory {DEPLOY_DIR} is missing. "
        "The exercise must begin with this directory present."
    )
    assert DEPLOY_DIR.is_dir(), f"{DEPLOY_DIR} exists but is not a directory."


def test_devices_txt_exists_and_content():
    # Presence & basic properties
    assert DEVICES_TXT.exists(), (
        f"Required file {DEVICES_TXT} is missing. "
        "Provisioning error: devices.txt must be present before any action."
    )
    assert DEVICES_TXT.is_file(), f"{DEVICES_TXT} exists but is not a regular file."

    # Content expectations
    raw = DEVICES_TXT.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:  # pragma: no cover
        raise AssertionError(f"{DEVICES_TXT} is not valid UTF-8.") from exc

    # Ensure final newline exists (POSIX convention)
    assert text.endswith("\n"), (
        f"{DEVICES_TXT} must end with a single newline character "
        "(this is required by the grading rubric)."
    )

    # Split lines & compare
    lines = text.splitlines()
    expected = ["127.0.0.1", "192.0.2.1"]
    assert lines == expected, (
        f"{DEVICES_TXT} must contain exactly two lines:\n"
        "  1. 127.0.0.1\n  2. 192.0.2.1\n"
        f"Found instead: {lines!r}"
    )


def test_no_diagnostics_directory_yet():
    """
    Before the student runs their solution, the diagnostics directory and its
    artefacts must NOT exist.  Their script is responsible for creating them.
    """
    assert not DIAG_DIR.exists(), (
        f"The diagnostics directory {DIAG_DIR} already exists. "
        "The pre-flight state should not contain any diagnostics artefacts."
    )


def test_no_preexisting_output_files():
    """
    Guard against accidental inclusion of artefacts that the grading script
    will produce.  Neither JSON nor CSV should be present yet.
    """
    for artefact in (SYSTEM_JSON, PING_CSV):
        assert not artefact.exists(), (
            f"Output file {artefact} should not exist before the student's "
            "solution runs."
        )