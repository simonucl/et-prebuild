# test_initial_state.py
#
# This pytest file asserts that none of the deliverables required by the
# assignment exist **before** the student begins working.  If any of these
# files are already present (or are dangling symlinks), the test suite will
# fail with a clear, actionable message so the learning platform can start
# from a predictable, clean slate.

from pathlib import Path
import os
import stat
import pytest


# --------- Helper utilities ------------------------------------------------- #
def _assert_absent(path: Path) -> None:
    """
    Assert that the given path does not exist in any form (regular file,
    directory, symlink, etc.).  The error message is crafted to be explicit
    so that the student or the platform can immediately see which file was
    pre-existing and thus violated the “clean slate” requirement.
    """
    assert not path.exists(), (
        f"Precondition failed: '{path}' already exists. "
        "The workspace must start empty; please remove the file/directory "
        "before running the assignment."
    )


# --------- Tests ------------------------------------------------------------ #
def test_ci_hosts_file_is_absent():
    """
    The hosts shim file must NOT exist yet.  The student will create it as
    part of the exercise.
    """
    _assert_absent(Path("/home/user/.ci_hosts"))


def test_resolve_script_is_absent():
    """
    The helper script must NOT exist yet.  The student will write it and make
    it executable.
    """
    _assert_absent(Path("/home/user/resolve_ci_hosts.sh"))


def test_dns_log_is_absent():
    """
    The one-shot DNS resolution log must NOT exist yet.  The student will
    generate it after the script works.
    """
    _assert_absent(Path("/home/user/dns_check.log"))