# test_initial_state.py
#
# This pytest suite validates that the workstation is still in its *pristine*
# state before the student carries out the FinOps configuration task.
#
# We intentionally assert that none of the artefacts required *after*
# completion of the task are present yet.  If any of them already exist (or
# already contain their final-state contents), the tests will fail with clear
# guidance so the learner can start from a clean slate.

from pathlib import Path
import pytest

# ----------------------------------------------------------------------------------------------------------------------
# Expected FINAL contents (for reference only – we check that they do *not* exist yet)
# ----------------------------------------------------------------------------------------------------------------------
EXPECTED_PROFILE_CONTENT = (
    "# FinOps environment settings\n"
    "export LANG=en_US.UTF-8\n"
    "export LC_ALL=en_US.UTF-8\n"
    "export TZ=America/New_York\n"
)

EXPECTED_LOG_CONTENT = (
    "FINOPS_PROFILE_STATUS: OK\n"
    "LANG=en_US.UTF-8\n"
    "LC_ALL=en_US.UTF-8\n"
    "TZ=America/New_York\n"
)

PROFILE_PATH = Path("/home/user/.finops_profile")
LOG_PATH = Path("/home/user/finops_profile_applied.log")

# ----------------------------------------------------------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------------------------------------------------------
def _assert_not_final_state(file_path: Path, expected_content: str) -> None:
    """
    Helper that fails if the file contains exactly the expected final-state
    bytes.  It passes when the file is absent or contains something different.
    """
    assert not (
        file_path.exists() and file_path.read_text(encoding="utf-8") == expected_content
    ), (
        f"{file_path} already exists with its FINAL required contents.\n"
        "The machine must start in a clean state so the student can practise "
        "creating this file from scratch.  Remove or rename it before running "
        "the exercise."
    )

@pytest.mark.order(1)
def test_finops_profile_is_absent_or_not_final():
    """
    /home/user/.finops_profile should *not* be present with its final contents
    before the task begins.
    """
    _assert_not_final_state(PROFILE_PATH, EXPECTED_PROFILE_CONTENT)

@pytest.mark.order(2)
def test_finops_log_is_absent_or_not_final():
    """
    /home/user/finops_profile_applied.log should *not* be present with its final
    contents before the task begins.
    """
    _assert_not_final_state(LOG_PATH, EXPECTED_LOG_CONTENT)