# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be present
# BEFORE the student starts the exercise.  Nothing related to the student’s
# future output (/home/user/security_scan, scan_report.log, …) is checked here.
#
# The repository under test is /home/user/repo/binaries  and must already
# contain exactly three regular files with specific contents and permission
# bits, as described in the task text.

import os
import stat
import hashlib
import pytest

REPO_DIR = "/home/user/repo/binaries"

# Ground-truth for files that have to be present
EXPECTED_FILES = {
    "lib1.jar": {
        "content": b"dummy jar content\n",
        "mode": 0o644,
    },
    "app.exe": {
        "content": b"malicious windows executable\n",
        "mode": 0o666,
    },
    "package.tar.gz": {
        "content": b"tgz archive placeholder\n",
        "mode": 0o644,
    },
}


def test_repository_directory_exists_and_is_directory():
    assert os.path.exists(REPO_DIR), (
        f"The repository directory {REPO_DIR} does not exist."
    )
    assert os.path.isdir(REPO_DIR), (
        f"{REPO_DIR} exists but is not a directory."
    )


def test_repository_contains_expected_files_and_no_extras():
    """The directory must contain exactly the expected files — no more, no less."""
    actual_files = sorted(
        f for f in os.listdir(REPO_DIR)
        if os.path.isfile(os.path.join(REPO_DIR, f))
    )
    expected_files_sorted = sorted(EXPECTED_FILES.keys())
    assert actual_files == expected_files_sorted, (
        "Repository file list mismatch.\n"
        f"Expected: {expected_files_sorted}\n"
        f"Found   : {actual_files}"
    )


@pytest.mark.parametrize("filename,truth", EXPECTED_FILES.items())
def test_each_file_has_expected_contents(filename, truth):
    """Validate byte-exact file contents."""
    path = os.path.join(REPO_DIR, filename)
    assert os.path.isfile(path), f"Missing file: {path}"
    with open(path, "rb") as fh:
        data = fh.read()
    assert data == truth["content"], (
        f"Content mismatch in {path!r}."
    )


@pytest.mark.parametrize("filename,truth", EXPECTED_FILES.items())
def test_each_file_has_expected_permissions(filename, truth):
    """Validate permission bits using four-digit octal notation."""
    path = os.path.join(REPO_DIR, filename)
    mode = stat.S_IMODE(os.stat(path).st_mode)
    expected_mode = truth["mode"]
    assert mode == expected_mode, (
        f"Permission mismatch for {path} — expected "
        f"{oct(expected_mode):>6} but found {oct(mode):>6}."
    )


@pytest.mark.parametrize("filename,truth", EXPECTED_FILES.items())
def test_sha256_matches_expected_contents(filename, truth):
    """
    Although the student will compute SHA-256 later, we confirm that the
    ground-truth content yields the same digest that downstream graders will
    expect.
    """
    path = os.path.join(REPO_DIR, filename)
    with open(path, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    expected_digest = hashlib.sha256(truth["content"]).hexdigest()
    assert digest == expected_digest, (
        f"SHA-256 mismatch for {path}."
    )