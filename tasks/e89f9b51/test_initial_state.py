# test_initial_state.py
#
# Pytest suite that validates the initial filesystem state required by the
# “disk-usage report” exercise _before_ the student starts working on it.
#
# The checks below confirm that the directory /home/user/test_env contains the
# exact structure and file sizes expected by the grader.  If anything is missing
# or has an unexpected size, the tests will fail with an explanatory message.
#
# NOTE:  ‑  These tests do **not** look for the student’s output file
#           (/home/user/disk_usage_report.json); they only validate the
#           pre-populated workspace.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants describing the expected filesystem layout                         #
# --------------------------------------------------------------------------- #

BASE_DIR = Path("/home/user/test_env").resolve()

EXPECTED_DIRECTORIES = {
    BASE_DIR / "app1": {
        BASE_DIR / "app1" / "config.yaml": 1200,
        BASE_DIR / "app1" / "data.bin": 20480,
        BASE_DIR / "app1" / "readme.txt": 600,
    },
    BASE_DIR / "app2": {
        BASE_DIR / "app2" / "config.ini": 900,
        BASE_DIR / "app2" / "core.dump": 51200,
        BASE_DIR / "app2" / "script.sh": 1500,
    },
    BASE_DIR / "logs": {
        BASE_DIR / "logs" / "app1.log": 30720,
        BASE_DIR / "logs" / "app2.log": 25600,
        BASE_DIR / "logs" / "archived" / "old.log": 10240,
    },
}

# Pre-computed directory totals that the grader is going to expect
EXPECTED_DIR_SIZES = {
    BASE_DIR / "app1": 22280,
    BASE_DIR / "app2": 53600,
    BASE_DIR / "logs": 66560,
}

# Five largest individual files the grader will look for
EXPECTED_TOP_5 = [
    (BASE_DIR / "app2" / "core.dump", 51200),
    (BASE_DIR / "logs" / "app1.log", 30720),
    (BASE_DIR / "logs" / "app2.log", 25600),
    (BASE_DIR / "app1" / "data.bin", 20480),
    (BASE_DIR / "logs" / "archived" / "old.log", 10240),
]

# --------------------------------------------------------------------------- #
# Helper functions                                                            #
# --------------------------------------------------------------------------- #

def dir_size_in_bytes(path: Path) -> int:
    """
    Recursively walk ``path`` and add up the size (in bytes) of every regular
    file it contains.  Symlinks are counted as the size of the link itself.
    """
    total = 0
    for root, _, files in os.walk(path):
        for name in files:
            fp = Path(root) / name
            try:
                total += fp.stat().st_size
            except FileNotFoundError:
                # If the file vanished between listing and stat (unlikely in this
                # controlled environment) – fail explicitly later on.
                pass
    return total


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_base_directory_exists():
    assert BASE_DIR.is_dir(), f"Expected base directory {BASE_DIR} to exist"


def test_expected_first_level_directories_present_and_nothing_extra():
    expected = {p.name for p in EXPECTED_DIRECTORIES}
    actual = {p.name for p in BASE_DIR.iterdir() if p.is_dir()}

    missing = expected - actual
    extra = actual - expected

    assert not missing, (
        "The following first-level directories are missing under "
        f"{BASE_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extra, (
        f"Unexpected directories found under {BASE_DIR}: "
        f"{', '.join(sorted(extra))} (only {', '.join(sorted(expected))} "
        "should be present)"
    )


@pytest.mark.parametrize(
    "directory_path, files_dict",
    sorted(EXPECTED_DIRECTORIES.items(), key=lambda i: i[0].name),
)
def test_expected_files_exist_with_correct_sizes(directory_path: Path, files_dict: dict):
    assert directory_path.is_dir(), f"Directory {directory_path} is missing"

    for file_path, expected_size in files_dict.items():
        assert file_path.is_file(), f"Expected file {file_path} to exist"

        actual_size = file_path.stat().st_size
        assert (
            actual_size == expected_size
        ), f"File {file_path} has size {actual_size} bytes, expected {expected_size} bytes"


@pytest.mark.parametrize(
    "directory_path, expected_total",
    sorted(EXPECTED_DIR_SIZES.items(), key=lambda i: i[0].name),
)
def test_directory_size_totals(directory_path: Path, expected_total: int):
    actual_total = dir_size_in_bytes(directory_path)
    assert (
        actual_total == expected_total
    ), (
        f"Directory size mismatch for {directory_path}.\n"
        f"  Expected: {expected_total} bytes\n"
        f"  Found:    {actual_total} bytes"
    )


def test_top_five_largest_files():
    # Build a list of every file under /home/user/test_env with its size
    all_files = []
    for root, _, files in os.walk(BASE_DIR):
        for name in files:
            fp = Path(root) / name
            size = fp.stat().st_size
            all_files.append((fp, size))

    # Sort according to the exact rules the grader will apply:
    #   1) descending size
    #   2) for ties, lexicographically by absolute path
    all_files_sorted = sorted(
        all_files,
        key=lambda t: (-t[1], str(t[0])),
    )

    top5 = all_files_sorted[:5]
    expected5 = EXPECTED_TOP_5

    # Build helpful error messages
    problems = []
    for idx, (actual, expected) in enumerate(zip(top5, expected5), start=1):
        actual_path, actual_size = actual
        expected_path, expected_size = expected
        if actual_path != expected_path or actual_size != expected_size:
            problems.append(
                f"Rank #{idx}: expected ({expected_path}, {expected_size}) "
                f"but found ({actual_path}, {actual_size})"
            )

    assert not problems, (
        "Top-5 largest files do not match the expected list:\n" + "\n".join(problems)
    )