# test_initial_state.py
#
# This pytest suite verifies that the operating-system / file-system
# are in their expected *initial* state – i.e. **before** the student
# performs any actions for the “policy-as-code via crontab” exercise.
#
# The required **final** state (after the student’s work) is:
#
#   1. The user-level crontab contains one and only one line:
#        15 */6 * * 1-5 /usr/local/bin/scan_secrets.sh --mode=ci-cd # DevSecOps policy
#      (…with a single trailing newline)
#
#   2. The file
#        /home/user/devsecops/policy/cron_baseline.log
#      exists and contains that exact same single line (plus newline).
#
# For the *starting* state, however, we must confirm that the system
# still needs configuration.  Therefore, this suite asserts that:
#
#   • Either the user has no crontab at all, **or**
#   • The crontab’s contents are *not yet* the single, policy-compliant line.
#
#   …and…
#
#   • Either the file /home/user/devsecops/policy/cron_baseline.log does
#     not exist, **or** it does exist but does *not* yet contain the
#     exact policy line.
#
# These checks guarantee that the student still has work to do and
# that any automated grader can safely evaluate their later actions.

import subprocess
from pathlib import Path

import pytest


# Constants describing the *final* desired artefact.
POLICY_LINE = (
    "15 */6 * * 1-5 /usr/local/bin/scan_secrets.sh --mode=ci-cd # DevSecOps policy\n"
)
POLICY_FILE = Path("/home/user/devsecops/policy/cron_baseline.log")


def _current_crontab():
    """
    Return a tuple: (has_crontab: bool, stdout_text: str)

    If the user has no crontab, has_crontab is False and stdout_text is ''.
    If the user has a crontab, has_crontab is True and stdout_text is the
    literal output of `crontab -l`.
    """
    proc = subprocess.run(
        ["crontab", "-l"],
        text=True,
        capture_output=True,
    )
    # When there is no crontab installed for the user, `crontab -l`
    # returns exit status 1 and prints e.g. "no crontab for user".
    if proc.returncode != 0:
        return False, ""
    return True, proc.stdout


def test_crontab_needs_creation_or_update():
    """
    Ensure that the user's crontab is either non-existent or *not yet*
    the single, policy-compliant line.
    """
    has_crontab, stdout_text = _current_crontab()

    if not has_crontab:
        # No crontab: this is an acceptable initial state.
        pytest.skip("User has no crontab yet – ready for student to create it.")

    # A crontab exists.  It must NOT already be exactly the required line.
    lines = [ln for ln in stdout_text.splitlines() if ln.strip()]

    assert not (
        len(lines) == 1 and stdout_text == POLICY_LINE
    ), (
        "The crontab already contains exactly the required single line; "
        "the student has nothing left to do.  The initial state should "
        "be empty or different so the task remains meaningful."
    )


def test_policy_file_absent_or_incorrect():
    """
    Ensure that the policy baseline file is either missing or does not
    yet contain the final, policy-compliant content.
    """
    if not POLICY_FILE.exists():
        pytest.skip(f"{POLICY_FILE} does not exist yet – ready for student to create it.")

    file_content = POLICY_FILE.read_text()

    assert (
        file_content != POLICY_LINE
    ), (
        f"{POLICY_FILE} already contains the exact policy line; "
        "the student appears to have completed the task prematurely. "
        "Initial state should require work."
    )