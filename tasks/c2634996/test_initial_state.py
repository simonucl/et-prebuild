# test_initial_state.py
#
# Validate the workstation *before* the student runs any commands.
# This suite asserts that the filesystem already contains the expected
# vulnerability–scan files and nothing more.  It deliberately does NOT
# reference the output file /home/user/scan_usage.log.

import os
import stat
from pathlib import Path
import pytest

HOME = Path("/home/user")
SCANS_DIR = HOME / "vuln_scans"

# Ground-truth metadata -------------------------------------------------------
EXPECTED_FILES = {
    "scan1.nmap": {
        "size": 5,
        "content": b"AAAA\n",
    },
    "scan2.nmap": {
        "size": 6,
        "content": b"BBBBB\n",
    },
    "errors.log": {
        "size": 6,
        "content": b"CCCCC\n",
    },
}

DIR_PERMS_OCT = 0o755
FILE_PERMS_OCT = 0o644


# Helper functions ------------------------------------------------------------
def _mode_bits(path: Path) -> int:
    "Return the permission bits (e.g. 0o755) of a file/directory."
    return stat.S_IMODE(path.stat().st_mode)


# Tests -----------------------------------------------------------------------
def test_scans_directory_exists_and_is_directory():
    assert SCANS_DIR.exists(), f"Required directory {SCANS_DIR} is missing."
    assert SCANS_DIR.is_dir(), f"{SCANS_DIR} exists but is not a directory."


def test_scans_directory_permissions():
    perms = _mode_bits(SCANS_DIR)
    assert (
        perms == DIR_PERMS_OCT
    ), f"{SCANS_DIR} has permissions {oct(perms)}, expected {oct(DIR_PERMS_OCT)}."


def test_scans_directory_contains_expected_files_only():
    actual_files = sorted(p.name for p in SCANS_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_FILES.keys())
    assert (
        actual_files == expected_files
    ), (
        f"{SCANS_DIR} should contain exactly these files:\n"
        f"  {expected_files}\n"
        f"but actually contains:\n"
        f"  {actual_files}"
    )

    # Ensure there are no sub-directories.
    subdirs = [p.name for p in SCANS_DIR.iterdir() if p.is_dir()]
    assert (
        not subdirs
    ), f"{SCANS_DIR} must not contain sub-directories, but found: {subdirs}"


@pytest.mark.parametrize("filename,meta", EXPECTED_FILES.items())
def test_each_file_exists_is_regular_and_has_correct_permissions_and_size(filename, meta):
    path = SCANS_DIR / filename
    assert path.exists(), f"Expected file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    perms = _mode_bits(path)
    assert (
        perms == FILE_PERMS_OCT
    ), f"{path} has permissions {oct(perms)}, expected {oct(FILE_PERMS_OCT)}."

    size = path.stat().st_size
    assert size == meta["size"], f"{path} should be {meta['size']} bytes, found {size} bytes."


@pytest.mark.parametrize("filename,meta", EXPECTED_FILES.items())
def test_each_file_has_exact_expected_content(filename, meta):
    path = SCANS_DIR / filename
    with path.open("rb") as fh:
        data = fh.read()
    assert (
        data == meta["content"]
    ), (
        f"Content of {path} is incorrect.\n"
        f"Expected: {meta['content']!r}\n"
        f"Found:    {data!r}"
    )


def test_total_bytes_truth_value():
    total_actual = sum((SCANS_DIR / fname).stat().st_size for fname in EXPECTED_FILES)
    total_expected = sum(meta["size"] for meta in EXPECTED_FILES.values())
    assert (
        total_actual == total_expected == 17
    ), f"Total byte count should be 17, found {total_actual}."