# test_initial_state.py
#
# This pytest file validates the **initial** operating-system / filesystem
# state *before* the student begins the exercise.  It checks that the raw
# diagnostic data files and working directories exist and that their
# contents match the specification.

import os
import re
import stat
import pytest

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

HOME = "/home/user"
RAW_DIR = os.path.join(HOME, "diag", "raw")
WORKING_DIR = os.path.join(HOME, "diag", "working")

MEM_LOG = os.path.join(RAW_DIR, "memory_stat.log")
DISK_LOG = os.path.join(RAW_DIR, "disk_stat.log")

# Expected numeric values from memory_stat.log
EXPECTED_MEM = {
    "MemTotal":      "8173400",
    "MemFree":       "204800",
    "MemAvailable":  "3500000",
}

# Expected values from disk_stat.log
EXPECTED_DISK = {
    "/dev/sda1": {"Size": "40G", "Used": "20G", "Avail": "18G"},
    "/dev/sda2": {"Size": "80G", "Used": "60G", "Avail": "18G"},
}

# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def _is_dir(path: str) -> None:
    """Assert that *path* exists and is a directory, and is writable by the user."""
    assert os.path.exists(path), f"Required directory {path!r} is missing."
    st_mode = os.stat(path).st_mode
    assert stat.S_ISDIR(st_mode), f"{path!r} exists but is not a directory."
    # User should have write permission (owner writable bit set)
    assert bool(st_mode & stat.S_IWUSR), f"Directory {path!r} is not writable by the user."


def _read_file_lines(path: str):
    """Return a list of lines (stripped of trailing newlines) from *path*."""
    with open(path, "r", encoding="utf-8") as fp:
        return [ln.rstrip("\n") for ln in fp.readlines()]


def _parse_kb_line(line: str):
    """
    From a line like 'MemTotal:       8173400 kB' return
    ('MemTotal', '8173400')
    """
    key_part, value_part = line.split(":", 1)
    # Remove all non-digit characters from the value part
    number = re.search(r"\d+", value_part)
    assert number, f"Cannot find numeric value in line: {line!r}"
    return key_part.strip(), number.group()


def _tokenise_disk_line(line: str):
    """
    Tokenise a 'df -h' output line into its fields.  Consecutive whitespace
    counts as one separator.
    """
    return re.split(r"\s+", line.strip())

# ---------------------------------------------------------------------------
# TESTS
# ---------------------------------------------------------------------------

def test_required_directories_exist_and_writable():
    """RAW and WORKING directories must exist and be writable."""
    _is_dir(RAW_DIR)
    _is_dir(WORKING_DIR)


def test_memory_stat_file_content():
    """memory_stat.log must contain the required key/value pairs."""
    assert os.path.isfile(MEM_LOG), f"Required file {MEM_LOG!r} is missing."

    lines = _read_file_lines(MEM_LOG)

    # Build a dict of the three required keys
    found = {}
    for ln in lines:
        if ln.startswith(("MemTotal:", "MemFree:", "MemAvailable:")):
            key, num = _parse_kb_line(ln)
            found[key] = num

    missing_keys = [k for k in EXPECTED_MEM if k not in found]
    assert not missing_keys, (
        f"memory_stat.log is missing the following keys: {', '.join(missing_keys)}"
    )

    for k, expected_val in EXPECTED_MEM.items():
        assert found[k] == expected_val, (
            f"Value for {k} in memory_stat.log is {found[k]!r}, expected {expected_val!r}"
        )


def test_disk_stat_file_content():
    """disk_stat.log must contain correct entries for /dev/sda1 and /dev/sda2."""
    assert os.path.isfile(DISK_LOG), f"Required file {DISK_LOG!r} is missing."

    lines = _read_file_lines(DISK_LOG)
    assert lines, "disk_stat.log appears to be empty."

    # First line should be a header starting with 'Filesystem'
    header = _tokenise_disk_line(lines[0])
    assert header[0] == "Filesystem", (
        "First line of disk_stat.log should start with 'Filesystem'"
    )

    # Find the column indices for Size, Used, Avail
    try:
        idx_size = header.index("Size")
        idx_used = header.index("Used")
        idx_avail = header.index("Avail")
    except ValueError as exc:
        raise AssertionError(
            "Header of disk_stat.log must contain 'Size', 'Used', and 'Avail' columns."
        ) from exc

    # Build a mapping: filesystem -> {Size, Used, Avail}
    found = {}
    for ln in lines[1:]:
        if not ln.strip():
            continue
        tokens = _tokenise_disk_line(ln)
        fs = tokens[0]
        if fs in EXPECTED_DISK:
            try:
                found[fs] = {
                    "Size": tokens[idx_size],
                    "Used": tokens[idx_used],
                    "Avail": tokens[idx_avail],
                }
            except IndexError:
                raise AssertionError(
                    f"Line for filesystem {fs!r} does not have enough columns."
                )

    # Ensure both required filesystems are present
    missing_fs = [fs for fs in EXPECTED_DISK if fs not in found]
    assert not missing_fs, (
        f"disk_stat.log is missing entries for the following filesystems: "
        f"{', '.join(missing_fs)}"
    )

    # Check each value
    for fs, exp_values in EXPECTED_DISK.items():
        for key, exp_val in exp_values.items():
            actual_val = found[fs][key]
            assert actual_val == exp_val, (
                f"For filesystem {fs}, column '{key}' is {actual_val!r}, "
                f"expected {exp_val!r}"
            )