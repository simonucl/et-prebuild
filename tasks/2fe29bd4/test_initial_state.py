# test_initial_state.py
#
# This pytest suite validates the *starting* filesystem state for the
# “FinOps month-end export” task _before_ the student performs any action.
#
# It checks that:
#   • the three expected raw CSV files exist (and nothing has been moved yet)
#   • their contents match the fixture data used by the grader
#   • file permissions are 0644
#   • the target directory /home/user/FinOps has **not** been created yet
#
# Only stdlib and pytest are used.

import os
from pathlib import Path
import stat
import pytest

HOME = Path("/home/user")
INCOMING = HOME / "incoming_reports"

EXPECTED_CSV_CONTENT = {
    "aws_costs_2023-09.csv": [
        "service,cost_usd",
        "EC2,25.50",
        "S3,7.25",
        "Lambda,2.40",
    ],
    "azure_costs_2023-09.csv": [
        "service,cost_usd",
        "VM,30.00",
        "Storage,5.75",
        "Functions,1.10",
    ],
    "gcp_costs_2023-09.csv": [
        "service,cost_usd",
        "ComputeEngine,18.60",
        "CloudStorage,6.90",
        "CloudFunctions,0.95",
    ],
}


def _mode(path: Path) -> int:
    """
    Return the permission bits (e.g. 0o644) for the given path,
    masking off the file-type information.
    """
    return path.stat().st_mode & 0o777


@pytest.mark.dependency(name="incoming_dir_exists")
def test_incoming_directory_exists_and_is_directory():
    assert INCOMING.exists(), (
        f"Required directory '{INCOMING}' is missing. "
        "The starting point must contain the incoming_reports folder with CSVs."
    )
    assert INCOMING.is_dir(), f"'{INCOMING}' exists but is not a directory."


@pytest.mark.dependency(depends=["incoming_dir_exists"], name="incoming_directory_contents")
def test_incoming_directory_contents_are_correct():
    """
    Check that all and only the three expected CSV files are present.
    Additional files would indicate that the workspace has been tampered with.
    """
    present_files = sorted(p.name for p in INCOMING.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_CSV_CONTENT.keys())

    missing = set(expected_files) - set(present_files)
    unexpected = set(present_files) - set(expected_files)

    assert not missing, (
        f"The following expected CSV file(s) are missing in '{INCOMING}': "
        + ", ".join(sorted(missing))
    )
    assert not unexpected, (
        f"Unexpected file(s) found in '{INCOMING}': " + ", ".join(sorted(unexpected))
    )


@pytest.mark.dependency(depends=["incoming_directory_contents"])
@pytest.mark.parametrize("filename,expected_lines", EXPECTED_CSV_CONTENT.items())
def test_each_csv_has_expected_contents_and_permissions(filename, expected_lines):
    """
    Validate both the content and the filesystem permissions (0644) for each CSV file.
    """
    path = INCOMING / filename
    assert path.exists(), f"Expected CSV file '{path}' is missing."
    assert path.is_file(), f"'{path}' exists but is not a regular file."

    # Check permissions
    assert _mode(path) == 0o644, (
        f"File '{path}' must have permissions 644, "
        f"but has {oct(_mode(path))} instead."
    )

    # Check content (ignore trailing newlines/whitespace)
    with path.open("r", encoding="utf-8") as fh:
        lines = [ln.rstrip("\n\r") for ln in fh.readlines()]

    assert lines == expected_lines, (
        f"File '{path}' does not match the expected fixture content.\n"
        "If the file was modified, reset it to the original state "
        "before attempting the task."
    )


def test_finops_directory_not_yet_created():
    """
    Before the student starts, /home/user/FinOps should **not** exist.
    This guarantees that the assessment of actions begins from a clean slate.
    """
    finops_dir = HOME / "FinOps"
    assert not finops_dir.exists(), (
        f"Directory '{finops_dir}' already exists, "
        "but it must be created by the student as part of the task. "
        "Remove or rename it before starting."
    )