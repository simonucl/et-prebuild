# test_initial_state.py
#
# Pytest test-suite that validates the *initial* operating-system / filesystem
# state **before** the student creates the automation script or any release
# artefacts.  If any of the following tests fail, the exercise starts from an
# unexpected environment and the student must not be graded on that basis.

import os
from pathlib import Path

import pytest

# --------------------------------------------------------------------------- #
# CONSTANTS                                                                   #
# --------------------------------------------------------------------------- #

HOME = Path("/home/user").resolve()
WS_ROOT = HOME / "workspace"
BUILD_OUTPUT = WS_ROOT / "build_output"
SCRIPTS_DIR = WS_ROOT / "scripts"
RELEASES_DIR = HOME / "releases"

EXPECTED_BUILD_FILES = {
    "app_binary": b"HelloAppBinaryV100",
    "libhelper.so": b"SharedObjectV100",
    "README.md": b"Build artifacts for release 1.0.0",
}

# --------------------------------------------------------------------------- #
# HELPERS                                                                     #
# --------------------------------------------------------------------------- #


def _read_exact_bytes(path: Path) -> bytes:
    """
    Read *all* bytes from `path` without stripping a trailing newline.
    """
    with path.open("rb") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# TESTS                                                                       #
# --------------------------------------------------------------------------- #


def test_build_output_directory_exists_with_expected_files():
    assert BUILD_OUTPUT.is_dir(), (
        f"Directory {BUILD_OUTPUT} is expected to exist but is missing."
    )

    actual_files = {p.name for p in BUILD_OUTPUT.iterdir() if p.is_file()}
    expected_files = set(EXPECTED_BUILD_FILES.keys())
    # Ensure there are **exactly** the three expected files—no more, no less.
    assert actual_files == expected_files, (
        f"{BUILD_OUTPUT} should contain exactly the files "
        f"{sorted(expected_files)}, but found {sorted(actual_files)}."
    )


@pytest.mark.parametrize("filename, expected_content", EXPECTED_BUILD_FILES.items())
def test_build_output_file_contents(filename, expected_content):
    file_path = BUILD_OUTPUT / filename
    assert file_path.is_file(), f"Expected file {file_path} is missing."

    data = _read_exact_bytes(file_path)
    assert (
        data == expected_content
    ), f"Contents of {file_path} differ from expectation."


def test_scripts_directory_exists_and_is_empty():
    assert SCRIPTS_DIR.is_dir(), f"Directory {SCRIPTS_DIR} should exist but does not."

    # The directory must be empty at the beginning of the exercise
    contents = [p.name for p in SCRIPTS_DIR.iterdir()]
    assert (
        contents == []
    ), f"{SCRIPTS_DIR} is expected to be empty, but contains: {sorted(contents)}."


def test_release_script_is_not_present_yet():
    script_path = SCRIPTS_DIR / "produce_release.sh"
    assert not script_path.exists(), (
        f"{script_path} should NOT exist at the start of the exercise."
    )


def test_releases_directory_does_not_exist_yet():
    assert not RELEASES_DIR.exists(), (
        f"Directory {RELEASES_DIR} must NOT exist before the script runs."
    )