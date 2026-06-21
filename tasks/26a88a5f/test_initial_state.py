# test_initial_state.py
#
# This test-suite validates that the initial filesystem state expected by the
# assignment is present *before* the student’s solution runs.
#
# It checks the following:
#   1. The workspace directory /home/user/ci_cd_workspace exists.
#   2. Exactly five direct sub-directories are present, with the expected names.
#   3. Each sub-directory contains the exact number of files documented in the
#      task description.
#   4. Every file has the precise byte-size that was promised.
#
# NOTE:
#   • The tests MUST NOT refer to any result/output files that the student is
#     supposed to create (e.g. /home/user/ci_disk_usage.log).  Consequently,
#     no assertion in this file touches that path.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the reference state                                    #
# --------------------------------------------------------------------------- #

WORKSPACE = Path("/home/user/ci_cd_workspace").resolve()

# Mapping: sub-dir name  ->  (expected_file_count, expected_single_file_size_in_bytes)
REFERENCE_LAYOUT = {
    "build_artifacts": (10, 100 * 1024),      # 100 KiB each
    "cache":           (3,  1 * 1024 * 1024), # 1  MiB each
    "logs":            (15, 20 * 1024),       # 20 KiB each
    "temp":            (5,  50 * 1024),       # 50 KiB each
    "scripts":         (2,  5 * 1024),        # 5  KiB each
}


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def _human_bytes(n: int) -> str:
    """Return a human-readable byte count to ease debugging messages."""
    kib = n / 1024
    if kib.is_integer():
        return f"{int(kib)} KiB"
    return f"{kib:.2f} KiB"


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_workspace_directory_exists():
    assert WORKSPACE.is_dir(), (
        f"Expected workspace directory {WORKSPACE} to exist, "
        "but it was not found."
    )


def test_workspace_contains_exact_subdirectories():
    expected_subdirs = set(REFERENCE_LAYOUT.keys())
    actual_subdirs   = {
        p.name for p in WORKSPACE.iterdir() if p.is_dir()
    }

    assert actual_subdirs == expected_subdirs, (
        "Workspace must contain exactly these sub-directories:\n"
        f"  {', '.join(sorted(expected_subdirs))}\n"
        f"Found instead:\n"
        f"  {', '.join(sorted(actual_subdirs))}"
    )


@pytest.mark.parametrize(
    "subdir, expected_count, expected_size",
    [(name, *values) for name, values in REFERENCE_LAYOUT.items()],
)
def test_each_subdir_file_count_and_sizes(subdir: str, expected_count: int, expected_size: int):
    """
    Verify that each reference sub-directory contains the exact number of
    files, and that every file has the precise byte size specified.
    """
    dir_path = WORKSPACE / subdir
    assert dir_path.is_dir(), (
        f"Expected directory {dir_path} to exist, but it was not found."
    )

    files = sorted(p for p in dir_path.iterdir() if p.is_file())

    # ------------- File count ------------------------------------------------
    assert len(files) == expected_count, (
        f"Directory {dir_path} should contain exactly {expected_count} files "
        f"but {len(files)} were found."
    )

    # ------------- File sizes ------------------------------------------------
    wrong_sizes = []
    for file in files:
        size = file.stat().st_size
        if size != expected_size:
            wrong_sizes.append((file.name, size))

    assert not wrong_sizes, (
        f"Some files in {dir_path} do not have the expected size "
        f"of {_human_bytes(expected_size)} ({expected_size} bytes):\n"
        + "\n".join(
            f"  - {fname}: {_human_bytes(sz)} ({sz} bytes)"
            for fname, sz in wrong_sizes
        )
    )