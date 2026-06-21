# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / file-system
# state **before** the student performs any action for the “environment-
# variable audit” exercise.
#
# What we expect to be present right now:
#   • Environment variables
#         SEC_KEY=abc123
#         COMPLIANCE_TOKEN=xyz789
#         SEC_LEVEL=low
#
# What we expect *not* to exist yet:
#   • /home/user/compliance/env_audit.log   (log file to be created)
#   • /home/user/compliance/.env           (baseline dotenv file to be created)
#   • A sourcing line in /home/user/.bashrc (“source /home/user/compliance/.env”)
#
# If any of these assumptions fail, the test suite will raise clear,
# descriptive errors so that the learner (or platform) knows what is wrong.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
COMPLIANCE_DIR = HOME / "compliance"
ENV_AUDIT_LOG = COMPLIANCE_DIR / "env_audit.log"
DOTENV = COMPLIANCE_DIR / ".env"
BASHRC = HOME / ".bashrc"
BASH_SOURCE_LINE = "source /home/user/compliance/.env"


# ----------  ENVIRONMENT VARIABLE CHECKS  --------------------------------- #


@pytest.mark.parametrize(
    "var, expected",
    [
        ("SEC_KEY", "abc123"),
        ("COMPLIANCE_TOKEN", "xyz789"),
        ("SEC_LEVEL", "low"),
    ],
)
def test_required_environment_variables_present(var, expected):
    """
    The container must export the preset SEC_/COMPLIANCE_ variables *before*
    the student starts.  The values must match exactly so that grading is
    deterministic.
    """
    assert var in os.environ, (
        f"Environment variable {var!r} is missing. "
        "The initial container must export it before the learner begins."
    )
    assert os.environ[var] == expected, (
        f"Environment variable {var!r} has value {os.environ[var]!r}, "
        f"but {expected!r} was expected."
    )


# ----------  FILE-SYSTEM CHECKS  ------------------------------------------ #


def test_compliance_directory_may_or_may_not_exist():
    """
    The /home/user/compliance directory is allowed to be absent (and usually
    will be).  If it *does* exist for some reason, it must *not* yet contain
    any of the files that the learner is supposed to create.
    """
    if COMPLIANCE_DIR.exists():
        # It must be a directory, not a file.
        assert COMPLIANCE_DIR.is_dir(), (
            f"{COMPLIANCE_DIR} exists but is not a directory."
        )
        # Ensure none of the target files already exist.
        assert not ENV_AUDIT_LOG.exists(), (
            f"{ENV_AUDIT_LOG} already exists, but the learner should create it."
        )
        assert not DOTENV.exists(), (
            f"{DOTENV} already exists, but the learner should create it."
        )


def test_bashrc_does_not_already_source_dotenv():
    """
    The learner’s task is to *append* a sourcing line to ~/.bashrc if it is
    missing.  Therefore, at the start of the exercise the line must not yet
    be present.
    """
    if not BASHRC.exists():
        # No .bashrc at all is also acceptable.
        pytest.skip(f"{BASHRC} does not exist yet; skipping check for source line.")

    # Read in a way that preserves newlines for accurate matching.
    with BASHRC.open("r", encoding="utf-8", errors="ignore") as fh:
        bashrc_content = fh.read().splitlines()

    # Assert that the specific line is not present.
    assert all(line.strip() != BASH_SOURCE_LINE for line in bashrc_content), (
        f"{BASHRC} already contains the compliance sourcing line:\n"
        f'    {BASH_SOURCE_LINE}\n'
        "It should not be present before the learner runs their solution."
    )


def test_no_premature_dotenv_file():
    """
    Ensure that the baseline dotenv file (.env) does not accidentally exist
    with the final contents or incorrect permissions before the learner runs
    the exercise.
    """
    assert not DOTENV.exists(), (
        f"{DOTENV} already exists. The learner must create it."
    )


def test_no_premature_env_audit_log():
    """
    Ensure that env_audit.log does not yet exist.  Creation and population of
    this file are part of the learner’s assignment.
    """
    assert not ENV_AUDIT_LOG.exists(), (
        f"{ENV_AUDIT_LOG} already exists. The learner must create it."
    )