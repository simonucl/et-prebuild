# test_initial_state.py
#
# This pytest suite validates that the initial operating-system / filesystem
# state is correct *before* the student performs any action.
#
# IMPORTANT
# ---------
# • These tests only check the **input** side of the task.  They intentionally
#   avoid looking for any output files or directories the student is expected
#   to create.
# • If any of these tests fail, the exercise is not set up correctly.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
RAW_DIR = HOME / "assessment" / "raw"
NMAP_FILE = RAW_DIR / "host1_nmap.txt"


def _read_nmap_file():
    """
    Helper that returns the content of the nmap file as a list of stripped
    lines.  Raises an AssertionError with a helpful message if the file
    cannot be read.
    """
    try:
        return NMAP_FILE.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(
            f"Required file not found: {NMAP_FILE}. "
            "Ensure it has been placed in the correct location."
        )
    except UnicodeDecodeError:  # pragma: no cover
        pytest.fail(
            f"Unable to decode {NMAP_FILE} as UTF-8. "
            "Make sure the file is plain-text UTF-8."
        )


def test_raw_directory_exists():
    assert RAW_DIR.exists(), (
        f"The directory {RAW_DIR} is missing.\n"
        "It must exist and contain the raw nmap scan results."
    )
    assert RAW_DIR.is_dir(), (
        f"{RAW_DIR} exists but is not a directory.\n"
        "It must be a directory that will house the raw input files."
    )


def test_nmap_file_exists_and_is_regular_file():
    assert NMAP_FILE.exists(), (
        f"The raw nmap scan file {NMAP_FILE} is missing.\n"
        "Place the file in the specified directory before the exercise begins."
    )
    assert NMAP_FILE.is_file(), (
        f"{NMAP_FILE} exists but is not a regular file.\n"
        "Ensure a plain-text nmap output file is present."
    )
    assert NMAP_FILE.stat().st_size > 0, (
        f"{NMAP_FILE} is empty.\n"
        "The file must contain the raw nmap scan results."
    )


def test_nmap_file_contains_expected_open_ports():
    """
    Basic sanity check on the content: we expect the file to contain at least
    the lines for the two open ports used in the task description.
    This guards against the file being swapped out or truncated.
    """
    lines = _read_nmap_file()

    # We look for substrings rather than exact full lines to allow for minor
    # variations in version strings while still ensuring the critical data is
    # present.
    required_substrings = [
        "22/tcp",
        "open",
        "ssh",
        "443/tcp",
        "open",
        "https",
        "Host is up",
        "Nmap scan report for",
    ]

    for substring in required_substrings:
        assert any(substring in line for line in lines), (
            f"The file {NMAP_FILE} does not appear to contain the expected "
            f"substring '{substring}'.\n"
            "Verify that the correct raw nmap output is present."
        )