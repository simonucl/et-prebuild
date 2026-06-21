# test_initial_state.py
#
# This pytest suite validates the **initial** state of the operating system
# before the student carries out the release-preparation task for “appcli”.
#
# What we verify:
#   1. /home/user/artifacts_staging exists and contains *exactly* the three
#      expected plaintext files (there must be no extras, not even hidden
#      “dot” files).
#   2. The three files have the correct *absolute* paths and are regular files.
#   3. /home/user/releases/v2.3.0 must **not** exist yet; neither may any of
#      its required payload files or the manifest.
#
# The tests fail early and clearly describe what is missing or unexpected.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

STAGING_DIR = Path("/home/user/artifacts_staging")
RELEASE_ROOT = Path("/home/user/releases/v2.3.0")

EXPECTED_STAGING_FILES = {
    STAGING_DIR / "appcli-2.3.0-linux-x86_64.bin",
    STAGING_DIR / "appcli-2.3.0-linux-arm64.bin",
    STAGING_DIR / "CHANGELOG-2.3.0.md",
}


def test_staging_directory_exists_and_is_dir():
    assert STAGING_DIR.exists(), f"Expected staging directory {STAGING_DIR} to exist."
    assert STAGING_DIR.is_dir(), f"{STAGING_DIR} exists but is not a directory."


def test_staging_directory_contains_exactly_expected_files():
    # Collect all *regular* files present directly in the staging directory
    present_files = {
        p for p in STAGING_DIR.iterdir() if p.is_file()
    }

    missing = EXPECTED_STAGING_FILES - present_files
    unexpected = present_files - EXPECTED_STAGING_FILES

    assert not missing, (
        "The following expected files are missing from the staging directory:\n"
        + "\n".join(str(p) for p in sorted(missing))
    )
    assert not unexpected, (
        "The staging directory contains unexpected files (only the three source "
        "files should be present at this point):\n"
        + "\n".join(str(p) for p in sorted(unexpected))
    )


def test_each_expected_file_is_regular_file():
    for path in EXPECTED_STAGING_FILES:
        assert path.exists(), f"Expected file {path} does not exist."
        assert path.is_file(), f"Expected {path} to be a regular file."


def test_release_root_does_not_exist_yet():
    assert not RELEASE_ROOT.exists(), (
        f"The release root {RELEASE_ROOT} should *not* exist before the "
        "student begins the task."
    )
    # The manifest must likewise be absent.
    manifest_path = RELEASE_ROOT / "manifest.txt"
    assert not manifest_path.exists(), (
        f"Manifest {manifest_path} should not exist before the task starts."
    )