# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state before the student
writes any code.

This file must be named exactly `test_initial_state.py` so that the grader
can discover it automatically.

Checks performed:
1. Presence of the expected build-output directories.
2. Presence of the expected single build artifact inside each directory.
3. Exact byte size of every artifact.
4. The cumulative size of each first-level build directory.
5. That the /home/user/output directory already exists and is writable.

None of the assertions look for the final report file
(/home/user/output/large_dirs.log); that file should not exist yet.
"""

import os
import stat
import pytest

# ---------- CONSTANTS --------------------------------------------------------

HOME = "/home/user"
BUILDS_ROOT = os.path.join(HOME, "builds")
OUTPUT_DIR = os.path.join(HOME, "output")

# Mapping: relative build-dir path  ->  expected artifact file name & byte size
EXPECTED_BUILD_CONTENT = {
    "android/app1": ("build_a.bin", 12288),
    "android/app2": ("build_b.bin", 4096),
    "ios/app1":     ("build_c.bin", 10240),
    "ios/app2_small": ("build_d.bin", 2048),
}

# Threshold for “large” directories (strictly greater than)
THRESHOLD = 9000


# ---------- HELPERS ----------------------------------------------------------

def rel_to_abs(rel_path: str) -> str:
    """Convert a path relative to BUILDS_ROOT into an absolute path."""
    return os.path.join(BUILDS_ROOT, rel_path)


def dir_size_bytes(abs_dir: str) -> int:
    """
    Recursively sum the sizes (in bytes) of all regular files contained
    in `abs_dir`.  Symlinks, device nodes, etc. are ignored.
    """
    total = 0
    for root, _dirs, files in os.walk(abs_dir, followlinks=False):
        for f in files:
            fp = os.path.join(root, f)
            try:
                st = os.lstat(fp)
            except FileNotFoundError:     # pragma: no cover
                continue                  # in case of a race, but unlikely
            # Only count regular files
            if stat.S_ISREG(st.st_mode):
                total += st.st_size
    return total


# ---------- TESTS ------------------------------------------------------------

def test_build_root_exists():
    assert os.path.isdir(BUILDS_ROOT), (
        f"Required directory '{BUILDS_ROOT}' is missing."
    )


@pytest.mark.parametrize("rel_dir, info", EXPECTED_BUILD_CONTENT.items())
def test_expected_directory_and_file_exist(rel_dir, info):
    artifact_name, expected_size = info
    abs_dir = rel_to_abs(rel_dir)
    abs_file = os.path.join(abs_dir, artifact_name)

    assert os.path.isdir(abs_dir), (
        f"Expected directory '{abs_dir}' is missing."
    )
    assert os.path.isfile(abs_file), (
        f"Expected file '{abs_file}' is missing."
    )

    actual_size = os.path.getsize(abs_file)
    assert actual_size == expected_size, (
        f"File '{abs_file}' should be {expected_size} bytes but is "
        f"{actual_size} bytes."
    )


@pytest.mark.parametrize("rel_dir, info", EXPECTED_BUILD_CONTENT.items())
def test_directory_cumulative_size(rel_dir, info):
    _, expected_artifact_size = info
    abs_dir = rel_to_abs(rel_dir)
    total_size = dir_size_bytes(abs_dir)

    # Because each directory contains exactly one artifact, the total
    # size must match the artifact size exactly.
    assert total_size == expected_artifact_size, (
        f"Cumulative size of directory '{abs_dir}' should be "
        f"{expected_artifact_size} bytes but is {total_size} bytes."
    )

    # Validate which directories are supposed to be “large”.
    is_large = total_size > THRESHOLD
    should_be_large = rel_dir in {"android/app1", "ios/app1"}

    assert is_large == should_be_large, (
        f"Directory '{abs_dir}' expected to be "
        f"{'>' if should_be_large else '<='} {THRESHOLD} bytes but "
        f"its calculated size is {total_size} bytes."
    )


def test_output_directory_exists_and_writable():
    assert os.path.isdir(OUTPUT_DIR), (
        f"Output directory '{OUTPUT_DIR}' is missing."
    )
    assert os.access(OUTPUT_DIR, os.W_OK), (
        f"Output directory '{OUTPUT_DIR}' is not writable."
    )