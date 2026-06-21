# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem state
# before the student performs any action for the “audit_cron” exercise.
#
# Expected pre-state (truth):
#   • /home/user/audit_cron   — must NOT exist (directory or file).
#   • User’s crontab is empty (no non-comment, non-blank lines).
#
# Only stdlib + pytest are used.

import os
import subprocess
from pathlib import Path

import pytest


HOME = Path("/home/user")
AUDIT_DIR = HOME / "audit_cron"


def test_audit_directory_absent():
    """
    /home/user/audit_cron must NOT exist before the student starts.
    """
    assert not AUDIT_DIR.exists(), (
        f"Pre-condition failed: {AUDIT_DIR} already exists. "
        "The exercise assumes the directory is created by the student."
    )


def _get_user_crontab_text():
    """
    Helper: returns (returncode, stdout, stderr) of `crontab -l`.
    """
    proc = subprocess.run(
        ["crontab", "-l"],
        capture_output=True,
        text=True,
        timeout=10,
    )
    return proc.returncode, proc.stdout, proc.stderr


def test_user_crontab_is_empty():
    """
    The default crontab for the user must be empty: either `crontab -l`
    returns a non-zero exit code (no crontab installed) *or* it returns
    only comments / blank lines.
    """
    rc, out, err = _get_user_crontab_text()

    if rc != 0:
        # Common message: "no crontab for user". This is acceptable pre-state.
        assert "no crontab" in err.lower() or err.strip() == "" or out.strip() == "", (
            "Unexpected error while reading crontab; got:\n"
            f"stdout: {out!r}\nstderr: {err!r}"
        )
    else:
        # Crontab exists; ensure it is effectively empty (only comments/blanks).
        meaningful_lines = [
            ln
            for ln in out.splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")
        ]
        assert (
            len(meaningful_lines) == 0
        ), "Pre-condition failed: user already has crontab entries:\n" + "\n".join(
            meaningful_lines
        )


@pytest.mark.parametrize(
    "rel_path",
    [
        "audit_cron/cron_security_audit.sh",
        "audit_cron/cron_audit.log",
        "audit_cron/setup_report.json",
    ],
)
def test_required_files_absent(rel_path):
    """
    None of the target files should exist before the student creates them.
    """
    path = HOME / rel_path
    assert not path.exists(), (
        f"Pre-condition failed: unexpected existing path {path}. "
        "The student must create this file during the exercise."
    )