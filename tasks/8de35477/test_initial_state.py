# test_initial_state.py
#
# This pytest suite confirms that the machine’s filesystem is in the
# expected “clean” state *before* the student runs any commands.
#
# It intentionally checks absolute paths only and fails with clear,
# actionable messages when something is missing or incorrect.
#
# NOTE: Do **not** modify this file.  It is executed automatically.

import os
from pathlib import Path

# ----------------------------------------------------------------------
# CONSTANTS – hard-coded paths & expected contents
# ----------------------------------------------------------------------

HOME                   = Path("/home/user")
RELEASE_DIR            = HOME / "release"
PACKAGES_DIR           = HOME / "packages"
STAGING_DIR            = HOME / "staging"

MANIFEST_PATH          = RELEASE_DIR / "manifest.txt"
LOGFILE_PATH           = RELEASE_DIR / "deployment_report_2024-01-01.txt"

EXPECTED_MANIFEST_LINES = [
    "app1-1.0.0.tar.gz\n",
    "app2-2.1.0.tar.gz\n",
    "app3-3.0.0.tar.gz\n",
    "readme.txt\n",
]

EXISTING_PACKAGES = [
    PACKAGES_DIR / "app1-1.0.0.tar.gz",
    PACKAGES_DIR / "app2-2.1.0.tar.gz",
]

MISSING_PACKAGES = [
    PACKAGES_DIR / "app3-3.0.0.tar.gz",
    PACKAGES_DIR / "readme.txt",
]

# ----------------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------------

def test_required_directories_exist():
    """
    /home/user/release, /home/user/packages, and /home/user/staging
    must already exist and be directories.
    """
    for path in (RELEASE_DIR, PACKAGES_DIR, STAGING_DIR):
        assert path.exists(), f"Required directory missing: {path}"
        assert path.is_dir(), f"Expected {path} to be a directory."


def test_manifest_exists_and_content_is_correct():
    assert MANIFEST_PATH.exists(), f"Manifest file is missing at {MANIFEST_PATH}"
    assert MANIFEST_PATH.is_file(), f"{MANIFEST_PATH} should be a regular file."

    # Read the entire file including newlines to make the comparison strict.
    with MANIFEST_PATH.open("r", encoding="utf-8") as fp:
        actual_lines = fp.readlines()

    assert actual_lines == EXPECTED_MANIFEST_LINES, (
        "Manifest content is incorrect.\n"
        f"Expected lines:\n{EXPECTED_MANIFEST_LINES!r}\n"
        f"Actual lines:\n{actual_lines!r}"
    )


def test_expected_packages_exist_and_are_non_empty():
    for pkg_path in EXISTING_PACKAGES:
        assert pkg_path.exists(), f"Expected package missing: {pkg_path}"
        assert pkg_path.is_file(),  f"{pkg_path} should be a regular file."
        assert pkg_path.stat().st_size > 0, f"{pkg_path} should not be empty."


def test_packages_that_should_be_missing_are_absent():
    for pkg_path in MISSING_PACKAGES:
        assert not pkg_path.exists(), (
            f"Package {pkg_path} should NOT exist yet, "
            "but it is present on the filesystem."
        )


def test_staging_directory_is_empty():
    contents = list(STAGING_DIR.iterdir())
    assert contents == [], (
        f"Staging directory {STAGING_DIR} is expected to be empty before the pipeline runs, "
        f"but it contains: {', '.join(map(str, contents))}"
    )


def test_log_file_does_not_exist_yet():
    assert not LOGFILE_PATH.exists(), (
        f"Deployment log {LOGFILE_PATH} should not exist before the pipeline runs."
    )