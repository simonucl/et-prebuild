# test_initial_state.py
#
# This pytest suite validates that the workspace is **clean** before the
# student begins the assignment “self-contained name-resolution workspace”.
#
# The student is expected to create everything under /home/user/dns_test,
# so at the very beginning that path (and any files inside it) must **not**
# exist.  These tests enforce that invariant.  If any test here fails, the
# system is in an unexpected state and the learner must reset before
# continuing.

import os
import stat
import subprocess
import pytest
from pathlib import Path

# Base workspace directory that must be absent before the student starts.
BASE_DIR = Path("/home/user/dns_test")

# All artefacts that the student will eventually create.
EXPECTED_PATHS = {
    BASE_DIR,
    BASE_DIR / "hosts_custom",
    BASE_DIR / "host_query.list",
    BASE_DIR / "resolve.log",
    BASE_DIR / "resolve_hosts.sh",
}


def _path_list_str(paths):
    """
    Helper: return a newline-joined list of stringified paths; used in
    assertion messages for clarity.
    """
    return "\n".join(str(p) for p in sorted(paths))


def test_base_directory_absent():
    """
    The directory /home/user/dns_test must NOT exist yet.  Its presence
    would indicate either that the student has already started the task
    or that the filesystem was not properly reset.
    """
    assert not BASE_DIR.exists(), (
        f"The directory {BASE_DIR} already exists, "
        "but the exercise requires starting from a clean slate.\n"
        "Remove it (and all its contents) before proceeding."
    )


@pytest.mark.parametrize("path", sorted(EXPECTED_PATHS - {BASE_DIR}))
def test_expected_files_absent(path: Path):
    """
    None of the artefacts that the learner is supposed to create should be
    present beforehand.  We parametrize over the list so that pytest reports
    each offending path individually.
    """
    assert not path.exists(), (
        f"The file {path} already exists.  The initial environment must not "
        "contain any of the target artefacts."
    )


def test_no_leftover_resolve_process():
    """
    Sanity check that no user-level process named 'resolve_hosts.sh' is
    already running.  This is not strictly required for the assignment, but
    catching it early avoids confusing behaviour when the student tests
    their own script.
    """
    try:
        # Use pgrep to look for processes whose command ends with
        # 'resolve_hosts.sh'.  The '-f' flag makes pgrep match the full
        # command line.  If pgrep finds something it exits 0.
        subprocess.run(
            ["pgrep", "-f", "resolve_hosts.sh"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        running = True
    except FileNotFoundError:
        # pgrep is part of procps; but if it's not available, skip the test.
        pytest.skip("pgrep not available on this system")
    except subprocess.CalledProcessError:
        # Exit code 1 ⇒ no matching process.
        running = False

    assert not running, (
        "A running process named 'resolve_hosts.sh' was detected.  "
        "Terminate it and ensure the environment is clean before starting."
    )


def test_home_directory_exists_and_is_dir():
    """
    Basic sanity: /home/user must exist and be a directory.  If this fails,
    the environment itself is mis-configured and the exercise cannot
    proceed.
    """
    home = Path("/home/user")
    assert home.exists(), "/home/user does not exist; environment is invalid."
    assert home.is_dir(), "/home/user exists but is not a directory."


def test_no_misplaced_hosts_file():
    """
    Check that there is no file named 'hosts_custom' elsewhere under
    /home/user that could be mistaken for the target file later.
    """
    home = Path("/home/user")
    misplaced = list(home.rglob("hosts_custom"))
    assert not misplaced, (
        "Found the following unexpected 'hosts_custom' files before the task "
        f"begins:\n{_path_list_str(misplaced)}\n"
        "Remove or rename them before proceeding."
    )