# test_initial_state.py
"""
Pytest suite that validates the **initial** operating-system / file-system state
_before_ the student runs their find/xargs solution for the “tidy-up a scattered
image dataset” exercise.

The tests deliberately **fail** if any prerequisite is missing or if the
dataset has already been modified.  They therefore guarantee a clean starting
point for the learner.

Only Python's standard library and `pytest` are used.
"""
from pathlib import Path
import os
import stat
import pytest
import pwd
import grp

HOME = Path("/home/user")
RAW_ROOT = HOME / "datasets" / "raw"
ORG_ROOT = HOME / "datasets" / "organized"

# --------------------------------------------------------------------------- #
# Reference data for the initial tree that must be in place.
# path (relative to RAW_ROOT) -> (size_bytes, mtime_epoch)
EXPECTED_FILES = {
    # projectA
    "projectA/img1.png":     (1_500_000, 1625097600),
    "projectA/img2.png":     (200_000,   1625184000),
    "projectA/old1.jpg":     (800_000,   1622505600),
    "projectA/note.txt":     (100,       1625270400),
    # projectB
    "projectB/big_graph.png": (2_500_000, 1625366400),
    "projectB/recent.jpg":    (600_000,   1627843200),
    "projectB/tiny.dat":      (300_000,   1625452800),
    # top-level
    "orphan.jpg": (700_000, 1622592000),
    "readme.md":  (4_000,   1625539200),
}

# Expected *directories* under RAW_ROOT (relative paths)
EXPECTED_DIRS = {
    ".",  # RAW_ROOT itself
    "projectA",
    "projectB",
}


# --------------------------------------------------------------------------- #
def assert_file_attributes(path: Path, expected_size: int, expected_mtime: int):
    """
    Helper: raises AssertionError with a clear message if the file at *path*
    does not exist or does not match the expected size / mtime to the second.
    """
    if not path.exists():
        pytest.fail(f"Required file is missing: {path}")
    if not path.is_file():
        pytest.fail(f"Expected a regular file but found something else: {path}")

    st = path.stat()
    size, mtime = st.st_size, int(st.st_mtime)

    assert size == expected_size, (
        f"File {path} has size {size} bytes, expected {expected_size}"
    )
    assert mtime == expected_mtime, (
        f"File {path} has mtime {mtime}, expected {expected_mtime}"
    )


# --------------------------------------------------------------------------- #
def test_raw_root_exists_and_is_directory():
    """/home/user/datasets/raw must exist and be a directory."""
    assert RAW_ROOT.exists(), f"{RAW_ROOT} does not exist."
    assert RAW_ROOT.is_dir(), f"{RAW_ROOT} exists but is not a directory."


@pytest.mark.parametrize(
    "relative_path, expected",
    [(rp, vals) for rp, vals in EXPECTED_FILES.items()],
)
def test_expected_files_present_with_correct_attributes(relative_path, expected):
    """
    Every path listed in EXPECTED_FILES must exist as a regular file and match
    its declared size & mtime.
    """
    full_path = RAW_ROOT / relative_path
    size, mtime = expected
    assert_file_attributes(full_path, size, mtime)


def test_no_unexpected_entries_in_raw_tree():
    """
    Ensures that /home/user/datasets/raw contains *only* the directories and
    files enumerated in EXPECTED_DIRS / EXPECTED_FILES.  This protects against
    stale data contaminating the exercise.
    """
    # Collect relative paths of everything under RAW_ROOT
    observed_files = set()
    observed_dirs = set()

    for dirpath, dirnames, filenames in os.walk(RAW_ROOT):
        rel_dir = Path(dirpath).relative_to(RAW_ROOT).as_posix() or "."
        observed_dirs.add(rel_dir)

        for fname in filenames:
            rel_file = Path(dirpath).relative_to(RAW_ROOT) / fname
            observed_files.add(rel_file.as_posix())

    # Directories
    unexpected_dirs = observed_dirs - EXPECTED_DIRS
    missing_dirs = EXPECTED_DIRS - observed_dirs
    assert not unexpected_dirs, (
        "Found unexpected directories inside RAW_ROOT: "
        + ", ".join(sorted(unexpected_dirs))
    )
    assert not missing_dirs, (
        "Missing expected directories inside RAW_ROOT: "
        + ", ".join(sorted(missing_dirs))
    )

    # Files
    unexpected_files = observed_files - set(EXPECTED_FILES.keys())
    missing_files = set(EXPECTED_FILES.keys()) - observed_files
    assert not unexpected_files, (
        "Found unexpected files inside RAW_ROOT: "
        + ", ".join(sorted(unexpected_files))
    )
    assert not missing_files, (
        "Missing expected files inside RAW_ROOT: "
        + ", ".join(sorted(missing_files))
    )


def test_organized_directory_not_yet_created():
    """
    The student has not run their solution yet, therefore the entire
    /home/user/datasets/organized hierarchy must be absent or empty.  If it
    exists and already contains files, the initial state is corrupt.
    """
    if not ORG_ROOT.exists():
        # Ideal case: directory not created yet.
        return

    # It exists – ensure it is empty.
    all_items = [p for p in ORG_ROOT.rglob("*") if p != ORG_ROOT]
    assert not all_items, (
        f"{ORG_ROOT} already exists and is not empty.  "
        "The environment is not in its initial state."
    )