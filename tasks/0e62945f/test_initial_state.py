# test_initial_state.py
#
# Pytest suite that validates the *initial* OS / filesystem state **before**
# the student performs any action for the “artifact-repository curator” task.
#
# This test file asserts that:
# 1. Mandatory directories exist with the correct permissions.
# 2. Source data files exist, carry the correct permission bits, and contain
#    the exact expected content (header + three data lines).
# 3. Output/side-effect files **do not** exist yet.
#
# All failures include clear, actionable explanations.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user").resolve()
REPOS_DIR = HOME / "repos"
LOGS_DIR = HOME / "logs"

PACKAGES_A = REPOS_DIR / "packages_a.txt"
PACKAGES_B = REPOS_DIR / "packages_b.txt"
MERGED_CSV = REPOS_DIR / "merged_packages.csv"
MERGE_LOG = LOGS_DIR / "merge_operation.log"

EXPECTED_A_LINES = [
    "build;sha256;size",
    "coreutils;f1c2d3e4;1200K",
    "openssl;abcd1234;3400K",
    "nginx;9876abcd;2500K",
]

EXPECTED_B_LINES = [
    "project;version;maintainer",
    "coreutils;9.3;gnu",
    "openssl;3.1.1;openssl",
    "nginx;1.25.0;nginx",
]

DIR_PERMS = 0o755
FILE_PERMS = 0o644


def _assert_mode(path: Path, expected_perm: int) -> None:
    """Assert that `path` has exactly the `expected_perm` permission bits."""
    mode = path.stat().st_mode & 0o777
    assert (
        mode == expected_perm
    ), f"{path} permission bits are {oct(mode)}, expected {oct(expected_perm)}."


@pytest.mark.parametrize(
    "directory",
    [
        REPOS_DIR,
        LOGS_DIR,
    ],
)
def test_directories_exist_with_correct_permissions(directory: Path):
    assert directory.exists(), f"Required directory {directory} is missing."
    assert directory.is_dir(), f"{directory} exists but is not a directory."
    _assert_mode(directory, DIR_PERMS)


@pytest.mark.parametrize(
    "file_path,expected_lines",
    [
        (PACKAGES_A, EXPECTED_A_LINES),
        (PACKAGES_B, EXPECTED_B_LINES),
    ],
)
def test_source_files_exist_have_correct_permissions_and_content(
    file_path: Path, expected_lines
):
    assert file_path.exists(), f"Required file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."
    _assert_mode(file_path, FILE_PERMS)

    # Read file and compare line-by-line **without** trailing newline chars
    with file_path.open("r", encoding="utf-8") as fp:
        actual_lines = [line.rstrip("\n") for line in fp]

    assert (
        actual_lines == expected_lines
    ), f"Content of {file_path} differs from expected.\nExpected lines:\n{expected_lines}\nActual lines:\n{actual_lines}"


@pytest.mark.parametrize(
    "unexpected_path",
    [
        MERGED_CSV,
        MERGE_LOG,
    ],
)
def test_no_output_files_exist_yet(unexpected_path: Path):
    assert (
        not unexpected_path.exists()
    ), f"{unexpected_path} should not exist before the merge operation is executed."