# test_initial_state.py
#
# This test-suite verifies the *initial* state of the operating system
# before the student has carried out the deployment task.
#
# WHAT **MUST NOT** YET EXIST
#   1. /home/user/deploy/release.sh ─ the deployment script.
#   2. /home/user/logs/cron_setup.log ─ the evidence log.
#   3. The exact cron entry
#        30 2 * * * /home/user/deploy/release.sh >> /home/user/deploy/release.log 2>&1
#      in the current user’s crontab.
#
# If any of the above are already present the test will fail so the student
# starts from a clean slate.
#
# NOTE:
# * Only Python’s standard library and pytest are used.
# * Explanatory failure messages guide the student.
# * No checks for any output artefacts that the student has yet to create.

import os
import shutil
import subprocess
from pathlib import Path

import pytest

HOME = Path("/home/user")
DEPLOY_SCRIPT = HOME / "deploy" / "release.sh"
EVIDENCE_LOG = HOME / "logs" / "cron_setup.log"
CRON_LINE = (
    "30 2 * * * /home/user/deploy/release.sh >> /home/user/deploy/release.log 2>&1"
)


def _get_user_crontab():
    """
    Safely fetch the current user’s crontab.

    Returns
    -------
    tuple[str, str]:
        stdout, stderr of `crontab -l`.
        If the user has no crontab an empty string is returned for stdout.
    """
    # `crontab -l` exits with
    #   * 0 if a crontab exists,
    #   * 1 and prints "no crontab for <user>" to stderr otherwise.
    #
    # We do *not* raise on non-zero return codes; we surface the raw output
    # so that the calling test can reason about it.
    result = subprocess.run(
        ["crontab", "-l"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout, result.stderr


def test_deploy_script_should_not_exist():
    assert not DEPLOY_SCRIPT.exists(), (
        f"The deployment script should not exist yet: {DEPLOY_SCRIPT}\n"
        "Please start from a clean environment."
    )


def test_evidence_log_should_not_exist():
    assert not EVIDENCE_LOG.exists(), (
        f"The evidence log should not exist yet: {EVIDENCE_LOG}\n"
        "Please start from a clean environment."
    )


def test_crontab_should_not_contain_target_line():
    stdout, stderr = _get_user_crontab()

    # If the user has *no* crontab the command prints a message to stderr
    # such as "no crontab for user", which is acceptable here.
    combined_output = "\n".join([stdout, stderr])

    # Whitespace-exact lookup
    contains_line = any(
        line.strip() == CRON_LINE for line in combined_output.splitlines()
    )

    assert not contains_line, (
        "The target cron entry is already present in the current user's crontab.\n"
        "Initial state must contain no such entry so the student can add it later.\n\n"
        f"Detected crontab output:\n{combined_output or '[no crontab]'}"
    )


@pytest.mark.parametrize(
    "path",
    [
        HOME / "deploy",
        HOME / "logs",
    ],
)
def test_directories_may_or_may_not_exist_but_are_clean(path):
    """
    The containing directories may already exist (e.g. provided by the grader),
    but if they do exist they must *not* yet contain the target artefacts.

    This test is mostly informative; it ensures we catch edge-cases where
    old artefacts were left behind in a shared workspace.
    """
    if not path.exists():
        pytest.skip(f"{path} directory does not exist yet (which is fine).")

    assert DEPLOY_SCRIPT.name not in os.listdir(path), (
        f"Directory {path} already contains {DEPLOY_SCRIPT.name}. "
        "The file should be created by the student."
    )
    assert EVIDENCE_LOG.name not in os.listdir(path), (
        f"Directory {path} already contains {EVIDENCE_LOG.name}. "
        "The file should be created by the student."
    )