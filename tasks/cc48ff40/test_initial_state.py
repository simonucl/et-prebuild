# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the filesystem for the
# “release-manager” exercise.  It makes sure that the source material the
# learner must work with already exists and that none of the artefacts the
# learner is supposed to create are present yet.  If any check fails the
# error message should make it obvious what is missing or unexpectedly
# present.

import datetime
from pathlib import Path

import pytest


HOME = Path("/home/user")
RELEASES_DIR = HOME / "releases"

ENVIRONMENTS_CSV = RELEASES_DIR / "environments.csv"
VERSIONS_TXT = RELEASES_DIR / "versions.txt"
DEPLOYMENT_PLAN = RELEASES_DIR / "deployment_plan.tsv"

LOGS_DIR = RELEASES_DIR / "logs"
DEPLOYMENT_LOG = LOGS_DIR / "deployment_actions.log"


# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    """Return text from *path* with universal newlines (LF only)."""
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


# --------------------------------------------------------------------------- #
# Tests for initial filesystem state
# --------------------------------------------------------------------------- #
def test_releases_directory_exists():
    assert RELEASES_DIR.is_dir(), f"Expected directory {RELEASES_DIR} to exist."


def test_source_files_exist_and_have_exact_content():
    # 1. environments.csv
    assert ENVIRONMENTS_CSV.is_file(), f"Missing source file: {ENVIRONMENTS_CSV}"
    expected_env_csv = (
        "env,owner\n"
        "prod,alice\n"
        "staging,bob\n"
        "qa,charlie\n"
    )
    actual_env_csv = read_text(ENVIRONMENTS_CSV)
    assert actual_env_csv == expected_env_csv, (
        f"File {ENVIRONMENTS_CSV} does not match the expected contents.\n"
        f"--- expected ---\n{expected_env_csv!r}\n"
        f"--- actual -----\n{actual_env_csv!r}\n"
    )

    # 2. versions.txt
    assert VERSIONS_TXT.is_file(), f"Missing source file: {VERSIONS_TXT}"
    expected_versions_txt = (
        "prod v2.3.1\n"
        "staging v2.3.1-rc\n"
        "qa v2.3.0\n"
    )
    actual_versions_txt = read_text(VERSIONS_TXT)
    assert actual_versions_txt == expected_versions_txt, (
        f"File {VERSIONS_TXT} does not match the expected contents.\n"
        f"--- expected ---\n{expected_versions_txt!r}\n"
        f"--- actual -----\n{actual_versions_txt!r}\n"
    )


def test_logs_directory_exists():
    assert LOGS_DIR.is_dir(), f"Expected directory {LOGS_DIR} to exist."


def test_deployment_plan_not_created_yet():
    assert not DEPLOYMENT_PLAN.exists(), (
        f"{DEPLOYMENT_PLAN} should NOT exist before the student runs their "
        "solution."
    )


def test_log_file_has_no_new_entry_yet():
    """
    The deployment log may or may not exist at the start.  If it does exist,
    it must NOT already contain a line ending with 'CREATED deployment_plan.tsv'
    dated today, because that is what the student is supposed to add.
    """
    today = datetime.date.today().isoformat()

    if not DEPLOYMENT_LOG.exists():
        pytest.skip(f"{DEPLOYMENT_LOG} does not exist yet — this is acceptable.")
        return  # pragma: no cover

    log_text = read_text(DEPLOYMENT_LOG).strip().splitlines()
    forbidden_line = f"{today} CREATED deployment_plan.tsv"
    assert forbidden_line not in log_text, (
        f"The log file {DEPLOYMENT_LOG} already contains the line that should "
        f"only be added by the student's solution:\n{forbidden_line!r}"
    )