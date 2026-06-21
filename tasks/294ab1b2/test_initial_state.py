# test_initial_state.py
#
# This test-suite validates that the starting filesystem state matches the
# expectations laid out in the assignment *before* the student’s script runs.
# It checks that the exact set of build artifacts is present (and **only**
# those artifacts), that every expected directory exists, that file sizes are
# correct, and that the build-report file has **not** yet been created.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# Constants                                                                   
# --------------------------------------------------------------------------- #

BASE_DIR = Path("/home/user/builds").resolve()

EXPECTED_DIRS = {
    BASE_DIR,
    BASE_DIR / "projectA",
    BASE_DIR / "projectB",
    BASE_DIR / "projectC",
    BASE_DIR / "old",
    BASE_DIR / "old" / "projectX",
}

# Mapping of absolute paths -> expected size in bytes
EXPECTED_FILES = {
    BASE_DIR / "projectA" / "artifact-1.0.0.tar.gz": 12_582_912,
    BASE_DIR / "projectA" / "artifact-1.0.0.sha256": 70,
    BASE_DIR / "projectB" / "artifact-2.1.3.tar.gz": 26_214_400,
    BASE_DIR / "projectB" / "artifact-2.1.3.doc.pdf": 3_145_728,
    BASE_DIR / "projectC" / "artifact-3.4.5.tar.gz": 8_388_608,
    BASE_DIR / "old" / "projectX" / "artifact-0.9.9.tar.gz": 41_943_040,
    BASE_DIR / "README.txt": 1_536,
}

BUILD_REPORT_DIR = Path("/home/user/build_report")
BUILD_REPORT_FILE = BUILD_REPORT_DIR / "disk_usage.log"


# --------------------------------------------------------------------------- #
# Helper utilities                                                            
# --------------------------------------------------------------------------- #
def all_files_under(directory: Path) -> set[Path]:
    """
    Return a set containing **absolute** Path objects for every regular file
    found anywhere under `directory`.
    """
    found: set[Path] = set()
    for root, _dirs, files in os.walk(directory):
        for f in files:
            found.add(Path(root, f).resolve())
    return found


# --------------------------------------------------------------------------- #
# Tests                                                                       
# --------------------------------------------------------------------------- #

def test_builds_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Directory {BASE_DIR} is expected to exist before the student script "
        "runs, but it was not found."
    )


def test_expected_directories_present_and_no_extras():
    # Presence of expected directories
    missing_dirs = {d for d in EXPECTED_DIRS if not d.is_dir()}
    assert not missing_dirs, (
        "The following expected directories are missing:\n"
        + "\n".join(str(p) for p in sorted(missing_dirs))
    )

    # Ensure there is no unexpected directory directly under BASE_DIR
    # (Sub-directories of the known ones are allowed.)
    top_level_actual = {p for p in BASE_DIR.iterdir() if p.is_dir()}
    allowed_top_level = {p for p in EXPECTED_DIRS if p.parent == BASE_DIR}
    extra_dirs = top_level_actual - allowed_top_level
    assert not extra_dirs, (
        "Unexpected directories found inside /home/user/builds:\n"
        + "\n".join(str(p) for p in sorted(extra_dirs))
    )


def test_expected_files_present_correct_size_and_no_extras():
    # --- presence and size -------------------------------------------------- #
    missing_files = [p for p in EXPECTED_FILES if not p.is_file()]
    assert not missing_files, (
        "The following expected files are missing:\n"
        + "\n".join(str(p) for p in sorted(missing_files))
    )

    size_mismatches = [
        f"{p} (expected {EXPECTED_FILES[p]}, found {p.stat().st_size})"
        for p in EXPECTED_FILES
        if p.is_file() and p.stat().st_size != EXPECTED_FILES[p]
    ]
    assert not size_mismatches, (
        "These files have an unexpected size:\n" + "\n".join(size_mismatches)
    )

    # --- exclusivity: ensure no extra files exist --------------------------- #
    actual_files = all_files_under(BASE_DIR)
    expected_files_set = set(EXPECTED_FILES.keys())
    extra_files = actual_files - expected_files_set
    assert not extra_files, (
        "Found files inside /home/user/builds that are *not* part of the "
        "expected initial state:\n"
        + "\n".join(str(p) for p in sorted(extra_files))
    )


def test_build_report_not_yet_created():
    """
    Prior to the student's work, the build report file must not exist.
    The directory itself may or may not exist, but the *file* definitely
    must be absent.
    """
    assert not BUILD_REPORT_FILE.exists(), (
        f"File {BUILD_REPORT_FILE} already exists, but it should be created "
        "by the student's solution."
    )