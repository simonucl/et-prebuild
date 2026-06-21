# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student runs their data–preparation script.
#
# What we assert (and ONLY these things, per the instructions):
# 1. Directory /home/user/raw_images/ exists.
# 2. Inside that directory the following four regular files exist
#    and are non-empty:
#       - cat.jpg
#       - dog.jpg
#       - bird.jpg
#       - logo.png
#
# We deliberately do NOT check anything related to /home/user/dataset/*
# because those paths belong to the *output* the student is about to
# create, and the rules explicitly forbid testing for them here.
#
# The tests use only Python’s standard library plus pytest.

import os
from pathlib import Path

RAW_DIR = Path("/home/user/raw_images")
EXPECTED_FILES = {
    "cat.jpg",
    "dog.jpg",
    "bird.jpg",
    "logo.png",
}


def _file_description(path: Path) -> str:
    """Return a human-readable description of a filesystem object."""
    if not path.exists():
        return f"{path} (missing)"
    if path.is_dir():
        return f"{path} (directory, not a file)"
    size = path.stat().st_size
    return f"{path} (size={size} bytes)"


def test_raw_images_directory_exists():
    """The source directory for the raw images must be present."""
    assert RAW_DIR.exists(), (
        f"Required directory {RAW_DIR} is missing. "
        "Create it (or ensure it is mounted) before running the preparation task."
    )
    assert RAW_DIR.is_dir(), (
        f"{RAW_DIR} exists but is not a directory. "
        "It must be a directory that will hold the raw image files."
    )


def test_expected_files_present_and_non_empty():
    """
    All four source files must exist and be non-empty before any processing starts.
    We do NOT care about additional files; we only guarantee that the required
    ones are available.
    """
    missing = []
    empty = []

    for filename in EXPECTED_FILES:
        file_path = RAW_DIR / filename
        if not file_path.exists():
            missing.append(str(file_path))
        elif not file_path.is_file():
            missing.append(f"{file_path} (exists but is not a regular file)")
        elif file_path.stat().st_size == 0:
            empty.append(str(file_path))

    # Build a clear, actionable assertion message.
    problems = []
    if missing:
        problems.append(
            "Missing required files:\n  " + "\n  ".join(missing)
        )
    if empty:
        problems.append(
            "Files exist but are empty (size == 0 bytes):\n  " + "\n  ".join(empty)
        )

    assert not problems, (
        "The initial training files are not in the expected state:\n"
        + "\n".join(problems)
    )