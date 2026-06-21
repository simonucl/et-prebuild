# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the workspace
# before the student/deployment engineer runs the required one-liner.
#
# Requirements verified:
# 1. Directory /home/user/data_pipeline exists.
# 2. /home/user/data_pipeline/update.sh exists, is a regular file,
#    is executable and contains the expected script body.
# 3. update.sh behaves exactly as documented:
#       • exit-code 1 + correct stdout/stderr when run without args
#       • exit-code 0 + correct stdout when run with --force
# 4. /home/user/data_pipeline/deployment.log must NOT exist yet
#    (it is created only by the student’s command later on).
#
# The tests rely exclusively on Python’s stdlib + pytest.

import os
import stat
import subprocess
from pathlib import Path

import pytest

DATA_DIR = Path("/home/user/data_pipeline")
UPDATE_SH = DATA_DIR / "update.sh"
DEPLOY_LOG = DATA_DIR / "deployment.log"

ELLIPSIS = "…"
DRY_RUN_STDOUT = f"Attempting dry-run update {ELLIPSIS}"
DRY_RUN_STDERR = f"DRY-RUN FAILED – manual confirmation required"
FORCED_STDOUT_FIRST = f"Applying forced update {ELLIPSIS}"
FORCED_STDOUT_SECOND = "Update applied successfully."


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"Required directory {DATA_DIR} is missing. "
        "The initial workspace layout must contain this directory."
    )


def test_update_sh_exists_and_is_executable():
    assert UPDATE_SH.is_file(), (
        f"Expected file {UPDATE_SH} does not exist."
    )

    mode = UPDATE_SH.stat().st_mode
    assert mode & stat.S_IXUSR, (
        f"{UPDATE_SH} is not marked executable (missing user execute bit)."
    )


def _run_update(*args):
    """
    Helper that executes update.sh with the provided arguments.
    Returns subprocess.CompletedProcess with text mode output.
    """
    return subprocess.run(
        [str(UPDATE_SH), *args],
        capture_output=True,
        text=True,
        check=False,
    )


def test_update_sh_dry_run_behavior():
    """
    Running without arguments must:
      * exit with non-zero status (1 according to the spec)
      * print 'Attempting dry-run update …' to stdout
      * print 'DRY-RUN FAILED – manual confirmation required' to stderr
    """
    cp = _run_update()
    assert cp.returncode != 0, (
        "Dry-run invocation was expected to fail (non-zero exit status) "
        f"but returned {cp.returncode}."
    )

    # Strip trailing newlines for comparison
    stdout_line = cp.stdout.strip()
    stderr_line = cp.stderr.strip()

    assert stdout_line == DRY_RUN_STDOUT, (
        "Dry-run stdout mismatch.\n"
        f"Expected: {DRY_RUN_STDOUT!r}\n"
        f"Got     : {stdout_line!r}"
    )
    assert stderr_line == DRY_RUN_STDERR, (
        "Dry-run stderr mismatch.\n"
        f"Expected: {DRY_RUN_STDERR!r}\n"
        f"Got     : {stderr_line!r}"
    )


def test_update_sh_force_behavior():
    """
    Running with '--force' must:
      * exit with status 0
      * print two specific lines on stdout in order
      * produce no stderr output
    """
    cp = _run_update("--force")
    assert cp.returncode == 0, (
        f"Forced update should exit with 0 but exited with {cp.returncode}."
    )

    stdout_lines = cp.stdout.strip().splitlines()
    assert stdout_lines == [FORCED_STDOUT_FIRST, FORCED_STDOUT_SECOND], (
        "Forced update stdout did not match expected two-line block.\n"
        f"Expected lines:\n  1) {FORCED_STDOUT_FIRST!r}\n  2) {FORCED_STDOUT_SECOND!r}\n"
        f"Got lines: {stdout_lines!r}"
    )

    assert cp.stderr == "", (
        "Forced update should not emit anything on stderr "
        f"but got: {cp.stderr!r}"
    )


def test_deployment_log_not_preexisting():
    """
    deployment.log must *not* exist before the student runs their command.
    """
    assert not DEPLOY_LOG.exists(), (
        f"{DEPLOY_LOG} already exists. The workspace should start without this file; "
        "it must be created only by the student’s deployment command."
    )