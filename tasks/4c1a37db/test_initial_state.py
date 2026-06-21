# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student performs any action for the “quick API diagnostic”
# exercise.  These checks guarantee that the mandatory source artefacts
# are present and correct.
#
# NOTE:  We deliberately do NOT examine /home/user/diagnostics or the
#        future quick_api_diag.log file—those are outputs that the
#        student must create.

import os
import json
import subprocess
import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
DATA_DIR = HOME / "data"
STATUS_FILE = DATA_DIR / "status.json"
VERSION_FILE = DATA_DIR / "version.json"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> str:
    """
    Read a text file as UTF-8 and return its exact contents.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_curl_is_available():
    """
    The student must use `curl` with the file:// URL scheme.  Verify that
    the binary exists and is runnable.
    """
    result = subprocess.run(
        ["curl", "--version"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert result.returncode == 0, (
        "The `curl` command is not available or not executable in the "
        "current environment—please install or fix your PATH."
    )


def test_data_directory_exists():
    """
    The /home/user/data directory—containing the two JSON files—must exist.
    """
    assert DATA_DIR.is_dir(), (
        f"Required directory missing: {DATA_DIR}. The exercise expects the "
        "original JSON files to live here."
    )


@pytest.mark.parametrize(
    "path,expected_json",
    [
        (STATUS_FILE, {"status": "ok"}),
        (VERSION_FILE, {"version": "1.3.7"}),
    ],
)
def test_required_json_files_present_with_correct_content(path: Path, expected_json):
    """
    Both JSON files must be present AND contain the exact expected data.
    We parse the JSON to ignore any optional trailing newline but will
    also fail fast if the file is missing or malformed.
    """
    assert path.is_file(), f"Required file missing: {path}"

    raw = _read_file(path)
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        pytest.fail(f"File {path} contains invalid JSON: {exc}")

    assert parsed == expected_json, (
        f"File {path} contains unexpected JSON.\n"
        f"Expected: {expected_json}\n"
        f"Found:    {parsed}"
    )

    # Additionally ensure there are no accidental extra keys.
    assert set(parsed.keys()) == set(expected_json.keys()), (
        f"File {path} contains extra keys not specified in the task."
    )