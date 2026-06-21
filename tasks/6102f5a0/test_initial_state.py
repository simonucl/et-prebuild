# test_initial_state.py
#
# This test-suite validates the machine’s *initial* state – i.e. **before**
# the learner adds the new cron job or creates any output files.
#
# What we verify:
# 1. The /home/user/finops directory exists and has the correct type.
# 2. The helper script /home/user/finops/cleanup_stale_resources.sh exists,
#    is a regular file, is executable, and contains the expected stub code.
# 3. The current (non-root) user’s crontab is empty of *active* entries
#    (no non-comment, non-blank lines).
#
# Nothing related to the *output* files/directories (e.g. cron_job_list.log,
# or the to-be-installed crontab line) is tested here, as per the
# specification.

import os
import stat
import subprocess
import pwd
import pytest

FINOPS_DIR = "/home/user/finops"
SCRIPT_PATH = f"{FINOPS_DIR}/cleanup_stale_resources.sh"


def _human_perms(mode: int) -> str:
    "Return an rwxrwxrwx string for an st_mode integer."
    return "".join(
        ("r" if mode & mask else "-")
        + ("w" if mode & (mask >> 1) else "-")
        + ("x" if mode & (mask >> 2) else "-")
        for mask in (0o400, 0o040, 0o004)
    )


def test_finops_directory_exists():
    assert os.path.exists(
        FINOPS_DIR
    ), f"Expected directory {FINOPS_DIR!r} to exist, but it does not."
    assert os.path.isdir(
        FINOPS_DIR
    ), f"Expected {FINOPS_DIR!r} to be a directory, but it is not."


def test_cleanup_script_exists_and_is_executable():
    assert os.path.exists(
        SCRIPT_PATH
    ), f"Expected script {SCRIPT_PATH!r} to exist, but it does not."
    assert os.path.isfile(
        SCRIPT_PATH
    ), f"Expected {SCRIPT_PATH!r} to be a regular file, but it is not."

    # Executable bit for *owner* must be set so the user can run it.
    st = os.stat(SCRIPT_PATH)
    is_exec_owner = bool(st.st_mode & stat.S_IXUSR)
    assert is_exec_owner, (
        f"The helper script {SCRIPT_PATH!r} is not executable by its owner "
        f"(permissions: {_human_perms(st.st_mode)})."
    )

    # Basic content check – ensures the learner starts from the correct stub.
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]

    expected_first_line = "#!/usr/bin/env bash"
    expected_second_line = 'echo "Cleaning up stale resources..."'
    assert lines[:2] == [
        expected_first_line,
        expected_second_line,
    ], (
        f"{SCRIPT_PATH!r} does not contain the expected stub content.\n"
        f"First two lines expected:\n"
        f"  1: {expected_first_line}\n"
        f"  2: {expected_second_line}\n"
        f"Actual lines:\n"
        + "\n".join(f"  {i+1}: {l}" for i, l in enumerate(lines[:2]))
    )


def test_user_crontab_is_initially_empty():
    """
    The initial crontab for the current user must have *no active entries*.
    Accept either:
      • `crontab -l` returns exit-code 1 with the customary
        “no crontab for <user>” message, OR
      • exit-code 0 with an empty file or comments only.
    """
    result = subprocess.run(
        ["crontab", "-l"], capture_output=True, text=True, check=False
    )

    # If exit code is non-zero, we expect it to be because there is no crontab.
    if result.returncode != 0:
        expected_phrase = "no crontab for"
        assert expected_phrase in result.stderr.lower(), (
            "Unexpected error running `crontab -l`:\n"
            f"returncode={result.returncode}\n"
            f"stdout={result.stdout!r}\n"
            f"stderr={result.stderr!r}"
        )
        return  # Nothing further to check – crontab is absent, which is OK.

    # Exit-code 0: we must verify the file has no *active* lines.
    active_lines = [
        line
        for line in result.stdout.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    assert (
        not active_lines
    ), "The current user’s crontab is expected to be empty, " "but found:\n" + "\n".join(active_lines)