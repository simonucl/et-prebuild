# test_initial_state.py
#
# This test-suite validates that the operating-system / filesystem
# is in the *expected starting state* before the learner performs
# any actions for the “policy backup” exercise.
#
# It verifies:
#   • The required source directory tree exists.
#   • The four expected “.policy” files are present (and *only* those).
#   • The exact byte contents of each file match the specification.
#   • None of the artefacts that the learner is supposed to create
#     (tar archive, checksum file, log file) exist yet.
#
# Failures will provide clear diagnostic messages so the learner
# immediately knows what is missing or unexpected.

import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
POLICY_ROOT = HOME / "compliance" / "policies"
ARCHIVE_DIR = HOME / "compliance" / "archive"

EXPECTED_RELATIVE_PATHS = [
    "./custom/third_party.policy",
    "./data_privacy.policy",
    "./incident_response.policy",
    "./network_security.policy",
]

# Mapping of relative path  -> expected byte content (including trailing \n)
EXPECTED_CONTENT = {
    "./data_privacy.policy": (
        b"Data Privacy Policy v1\n"
        b"Approved: 2023-07-15\n"
    ),
    "./incident_response.policy": (
        b"Incident Response Policy v1\n"
        b"Approved: 2023-07-17\n"
    ),
    "./network_security.policy": (
        b"Network Security Policy v1\n"
        b"Approved: 2023-07-16\n"
    ),
    "./custom/third_party.policy": (
        b"Third Party Risk Policy v1\n"
        b"Approved: 2023-07-18\n"
    ),
}

# Paths that *should not* exist until the learner creates them.
TAR_PATH = ARCHIVE_DIR / "policy_backup_20240315.tar.gz"
SHA_PATH = ARCHIVE_DIR / "policy_backup_20240315.sha256"
LOG_PATH = ARCHIVE_DIR / "policy_backup_20240315.log"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _all_policy_files(root: Path):
    """
    Recursively walk `root` and return a list of all paths (relative to `root`)
    that have the `.policy` extension, sorted for determinism.
    """
    results = []
    for path in root.rglob("*.policy"):
        rel = f"./{path.relative_to(root).as_posix()}"
        results.append(rel)
    return sorted(results)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_policy_root_directory_exists_and_is_directory():
    assert POLICY_ROOT.exists(), (
        f"Expected directory {POLICY_ROOT} does not exist. "
        "The exercise requires this source directory."
    )
    assert POLICY_ROOT.is_dir(), (
        f"{POLICY_ROOT} exists but is not a directory."
    )


def test_expected_policy_files_present_and_no_extras():
    found = _all_policy_files(POLICY_ROOT)
    assert found, "No '.policy' files were found under the policies directory."
    assert found == sorted(EXPECTED_RELATIVE_PATHS), (
        "Mismatch in '.policy' files under the policies directory.\n"
        f"Expected exactly these files:\n  {EXPECTED_RELATIVE_PATHS}\n"
        f"Found:\n  {found}"
    )


@pytest.mark.parametrize("relative_path", EXPECTED_RELATIVE_PATHS)
def test_policy_file_contents_match_spec(relative_path):
    src_path = POLICY_ROOT / Path(relative_path[2:])  # strip leading "./"
    assert src_path.is_file(), f"Expected file {src_path} is missing."

    expected_bytes = EXPECTED_CONTENT[relative_path]
    got_bytes = src_path.read_bytes()
    assert got_bytes == expected_bytes, (
        f"Content of {src_path} differs from specification.\n"
        "Ensure the initial fixture files are correct."
    )


def test_archive_outputs_do_not_yet_exist():
    """
    Before the learner runs their solution, none of the required output
    artefacts should be present.  This test guards against stale files from
    a previous run leaking into the assessment environment.
    """
    for path in (TAR_PATH, SHA_PATH, LOG_PATH):
        assert not path.exists(), (
            f"Output artefact {path} already exists before the task starts. "
            "The environment should start clean."
        )