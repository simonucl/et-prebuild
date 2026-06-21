# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student carries out the backup-PKI task.
#
# The checks make sure nothing from the end-state already exists while the
# basic tooling (OpenSSL & coreutils) that the student needs is available.
#
# Only Python stdlib + pytest are used.

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

HOME = Path("/home/user")
WORK_DIR = HOME / "backup-work"
BUNDLE_DIR = WORK_DIR / "bundle"
ARCHIVES_DIR = HOME / "archives"

DATE_STAMP = "20240323"
TAR_GZ = ARCHIVES_DIR / f"cert-backup-{DATE_STAMP}.tar.gz"
MANIFEST = ARCHIVES_DIR / f"cert-backup-{DATE_STAMP}.manifest.csv"

PKI_ARTIFACTS = [
    WORK_DIR / "rootCA.key",
    WORK_DIR / "rootCA.crt",
    WORK_DIR / "server.key",
    WORK_DIR / "server.csr",
    WORK_DIR / "server.crt",
    BUNDLE_DIR / "rootCA.crt",
    BUNDLE_DIR / "server.crt",
]


# ---------- Helper utilities ----------


def _binary_exists(cmd_name: str) -> bool:
    """Return True iff *cmd_name* is found somewhere on $PATH."""
    return shutil.which(cmd_name) is not None


def _path_list_repr(paths):
    """Pretty helper for human-readable failure messages."""
    return "\n".join(f" - {p}" for p in paths)


# ---------- Tests ----------


def test_home_directory_present_and_writable():
    assert HOME.is_dir(), f"Expected home directory {HOME} to exist."
    test_file = HOME / ".pytest_write_test"
    try:
        with test_file.open("w") as fp:
            fp.write("ok")
    finally:
        try:
            test_file.unlink()
        except FileNotFoundError:
            pass


@pytest.mark.parametrize("cmd_name", ["openssl", "tar", "gzip", "sha256sum", "stat", "sort"])
def test_required_system_commands_exist(cmd_name):
    assert _binary_exists(
        cmd_name
    ), f'Required command "{cmd_name}" not found on PATH; please install coreutils/openssl.'


def test_working_tree_absent_initially():
    assert (
        not WORK_DIR.exists()
    ), f"Working directory {WORK_DIR} should NOT exist before the task begins."


def test_archives_directory_absent_initially():
    assert (
        not ARCHIVES_DIR.exists()
    ), f"Archive directory {ARCHIVES_DIR} should NOT exist before the task begins."


def test_expected_files_do_not_exist_yet():
    missing = [p for p in PKI_ARTIFACTS if p.exists()]
    assert not missing, (
        "None of the PKI artefacts should be present at the start, "
        "but the following were found:\n" + _path_list_repr(missing)
    )


def test_archive_and_manifest_absent():
    leftovers = [p for p in (TAR_GZ, MANIFEST) if p.exists()]
    assert not leftovers, (
        "The archive/manifest must NOT be present before execution, "
        "yet the following were found:\n" + _path_list_repr(leftovers)
    )