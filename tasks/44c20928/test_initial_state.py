# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state for the
# “spring-cleaning” exercise.  All tests must pass *before* the student
# runs any commands.  Failures will tell the student exactly what is
# missing or incorrect.
#
# The reference tree that **must** exist **verbatim** before the exercise:
#
# /home/user/storage/
# ├── archive/                     (present, EMPTY)
# └── incoming/
#     ├── emptydir/                (completely empty)
#     ├── project1/
#     │   ├── keep.txt   –  3  days old,   56  B
#     │   ├── large.bak  –  2  days old, 1.5 MiB
#     │   └── old.txt    – 15  days old,   42  B
#     └── project2/
#         ├── archive.txt – 12 days old,   73  B
#         └── temp2.bak   –  1 day  old, 1.28 MiB
#
# Only stdlib + pytest are used.

import os
import time
from pathlib import Path

import pytest

HOME = Path("/home/user")
STORAGE = HOME / "storage"
ARCHIVE = STORAGE / "archive"
INCOMING = STORAGE / "incoming"

# -----------------------------------------------------------------------------
# Helper predicates
# -----------------------------------------------------------------------------
ONE_MIB = 1_048_576            # 1 MiB in bytes
DAY     = 24 * 60 * 60         # seconds in a day


def seconds_ago(path: Path) -> float:
    """Return how many seconds ago *path* was modified."""
    return time.time() - path.stat().st_mtime


# -----------------------------------------------------------------------------
# 1. Basic directory layout
# -----------------------------------------------------------------------------
def test_root_directories_exist():
    assert STORAGE.is_dir(), f"{STORAGE!s} is missing"
    assert ARCHIVE.is_dir(), f"{ARCHIVE!s} is missing"
    assert INCOMING.is_dir(), f"{INCOMING!s} is missing"


# -----------------------------------------------------------------------------
# 2. `archive/` must be present **and empty**
# -----------------------------------------------------------------------------
def test_archive_is_empty():
    contents = list(ARCHIVE.iterdir())
    assert contents == [], (
        f"{ARCHIVE} must be EMPTY at start, found: "
        f"{[p.name for p in contents]}"
    )


# -----------------------------------------------------------------------------
# 3. `incoming/` sub-tree must contain exactly the expected directories/files
# -----------------------------------------------------------------------------
def test_incoming_structure():
    expected_dirs = {"emptydir", "project1", "project2"}
    found_dirs = {p.name for p in INCOMING.iterdir() if p.is_dir()}
    assert found_dirs == expected_dirs, (
        f"{INCOMING} should contain directories {sorted(expected_dirs)}, "
        f"found {sorted(found_dirs)}"
    )

    # ---------- project1 ----------
    project1 = INCOMING / "project1"
    exp_p1_files = {"keep.txt", "large.bak", "old.txt"}
    found_p1 = {p.name for p in project1.iterdir() if p.is_file()}
    assert found_p1 == exp_p1_files, (
        f"{project1} should contain files {sorted(exp_p1_files)}, "
        f"found {sorted(found_p1)}"
    )

    # ---------- project2 ----------
    project2 = INCOMING / "project2"
    exp_p2_files = {"archive.txt", "temp2.bak"}
    found_p2 = {p.name for p in project2.iterdir() if p.is_file()}
    assert found_p2 == exp_p2_files, (
        f"{project2} should contain files {sorted(exp_p2_files)}, "
        f"found {sorted(found_p2)}"
    )

    # ---------- emptydir ----------
    emptydir = INCOMING / "emptydir"
    assert emptydir.is_dir(), f"{emptydir} directory is missing"
    assert list(emptydir.iterdir()) == [], f"{emptydir} must be empty"


# -----------------------------------------------------------------------------
# 4. File-size expectations
# -----------------------------------------------------------------------------
def test_file_sizes():
    sizes = {
        "keep.txt":       56,
        "large.bak":  1_572_864,   # 1.5 MiB (1536 KiB)
        "old.txt":        42,
        "archive.txt":    73,
        "temp2.bak": 1_310_720,    # 1.28 MiB (1280 KiB)
    }

    # project1
    p1 = INCOMING / "project1"
    for fname in ("keep.txt", "large.bak", "old.txt"):
        f = p1 / fname
        assert f.is_file(), f"{f} is missing"
        real_size = f.stat().st_size
        exp_size = sizes[fname]
        assert real_size == exp_size, (
            f"{f} should be {exp_size} bytes, got {real_size}"
        )

    # project2
    p2 = INCOMING / "project2"
    for fname in ("archive.txt", "temp2.bak"):
        f = p2 / fname
        assert f.is_file(), f"{f} is missing"
        real_size = f.stat().st_size
        exp_size = sizes[fname]
        assert real_size == exp_size, (
            f"{f} should be {exp_size} bytes, got {real_size}"
        )

    # Convenience: assert *exactly two* >1 MiB “.bak” files exist (the targets)
    big_baks = [
        p for p in INCOMING.rglob("*.bak") if p.stat().st_size > ONE_MIB
    ]
    assert len(big_baks) == 2, (
        "Exactly two .bak files larger than 1 MiB must be present at start; "
        f"found {len(big_baks)}: {[str(p) for p in big_baks]}"
    )


# -----------------------------------------------------------------------------
# 5. Modification-time expectations (coarse but sufficient)
# -----------------------------------------------------------------------------
@pytest.mark.parametrize(
    "relative_path, min_days_ago, max_days_ago",
    [
        ("incoming/project1/keep.txt",      2,   5),   # ≈3 days
        ("incoming/project1/large.bak",     1,   4),   # ≈2 days
        ("incoming/project1/old.txt",      12,  20),   # ≈15 days
        ("incoming/project2/archive.txt",  10,  15),   # ≈12 days
        ("incoming/project2/temp2.bak",     0,   3),   # ≈1 day
    ],
)
def test_file_mtime_windows(relative_path, min_days_ago, max_days_ago):
    """
    Assert that each file's modification time falls within a reasonable
    window around the reference ages described in the exercise.  We use
    broad ranges to accommodate small timing differences.
    """
    path = STORAGE / relative_path
    assert path.is_file(), f"{path} is missing"

    age_days = seconds_ago(path) / DAY
    assert min_days_ago <= age_days <= max_days_ago, (
        f"{path} should be between {min_days_ago} and {max_days_ago} days old; "
        f"got {age_days:.1f} days"
    )


# -----------------------------------------------------------------------------
# 6. Sanity checks for counts used in the later steps
# -----------------------------------------------------------------------------
def test_cts_for_coming_operations():
    """
    Cross-check that the counts used in the forthcoming maintenance script
    are indeed correct in the initial tree.
    """
    # (a) Number of .bak files >1 MiB
    big_baks = [
        p for p in INCOMING.rglob("*.bak") if p.stat().st_size > ONE_MIB
    ]
    assert len(big_baks) == 2, (
        "Step #1 expects to delete **exactly two** .bak files larger than "
        "1 MiB; initial tree must contain 2, found "
        f"{len(big_baks)}: {[str(p) for p in big_baks]}"
    )

    # (b) Number of .txt files older than 10 days
    old_txts = [
        p
        for p in INCOMING.rglob("*.txt")
        if seconds_ago(p) > 10 * DAY
    ]
    assert len(old_txts) == 2, (
        "Step #2 expects to move **exactly two** .txt files older than 10 days; "
        f"found {len(old_txts)}: {[str(p) for p in old_txts]}"
    )

    # (c) Number of empty directories in incoming/ (at least one: emptydir)
    empty_dirs = [
        d for d in INCOMING.rglob("*") if d.is_dir() and not any(d.iterdir())
    ]
    assert (INCOMING / "emptydir") in empty_dirs, (
        f"{INCOMING/'emptydir'} must be present and empty"
    )
    # We do not assert the exact count beyond containing emptydir; the script
    # only guarantees removal of *one* directory in the reference data set.


# -----------------------------------------------------------------------------
# End of file
# -----------------------------------------------------------------------------