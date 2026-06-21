# test_initial_state.py
#
# This pytest suite validates the *initial* state of the filesystem
# before the student begins working on the DevSecOps exercise.
# It checks that the required directory tree exists and that the
# CSV input file is present and contains the exact expected data.
#
# NOTE:  This file intentionally does **not** test for the presence
#        (or absence) of any output artifacts such as
#        allowed_ports.json or compliance.log.  Those belong to the
#        *final* state after the exercise is completed.

import os
import stat
import pytest

BASE_DIR = "/home/user/devsecops"
INPUT_DIR = os.path.join(BASE_DIR, "policy_input")
OUTPUT_DIR = os.path.join(BASE_DIR, "policy_output")
LOG_DIR = os.path.join(BASE_DIR, "logs")
CSV_PATH = os.path.join(INPUT_DIR, "services.csv")

EXPECTED_CSV_LINES = [
    "service,port,protocol,approved",
    "ssh,22,tcp,yes",
    "http,80,tcp,yes",
    "telnet,23,tcp,no",
    "smtp,25,tcp,yes",
    "ftp,21,tcp,no",
]


def assert_is_directory(path: str) -> None:
    """
    Helper: assert that `path` exists and is a directory.
    """
    assert os.path.exists(path), f"Expected directory {path!r} does not exist."
    # We want to be certain it's a directory, not a file or symlink.
    mode = os.stat(path, follow_symlinks=False).st_mode
    assert stat.S_ISDIR(mode), f"Path {path!r} exists but is not a directory."


def test_directory_structure_exists() -> None:
    """
    Verify that the required directory tree is in place.
    """
    assert_is_directory(BASE_DIR)
    assert_is_directory(INPUT_DIR)
    assert_is_directory(OUTPUT_DIR)
    assert_is_directory(LOG_DIR)


def test_services_csv_exists_with_expected_contents() -> None:
    """
    Ensure that services.csv exists at the expected location and that its
    contents match the specification exactly (six lines: one header + five
    records, comma-separated).
    """
    # 1. Existence and type
    assert os.path.exists(CSV_PATH), f"Input CSV file {CSV_PATH!r} is missing."
    assert os.path.isfile(CSV_PATH), f"{CSV_PATH!r} exists but is not a file."

    # 2. Read file
    with open(CSV_PATH, "r", encoding="utf-8") as fp:
        raw_contents = fp.read()

    # 3. Split into lines *without* retaining line terminators so we can compare
    #    agnostic of whether the final newline is present.
    actual_lines = raw_contents.splitlines()

    # 4. Exact match
    assert (
        actual_lines == EXPECTED_CSV_LINES
    ), (
        "The contents of services.csv do not match the expected template.\n\n"
        "Expected lines:\n"
        + "\n".join(EXPECTED_CSV_LINES)
        + "\n\nActual lines:\n"
        + "\n".join(actual_lines)
        + "\n"
    )

    # 5. Basic sanity checks on CSV shape (redundant but illustrative)
    header = actual_lines[0].split(",")
    expected_header = ["service", "port", "protocol", "approved"]
    assert (
        header == expected_header
    ), f"CSV header {header} does not match expected {expected_header}."

    for idx, row in enumerate(actual_lines[1:], start=2):  # 1-based, include header
        columns = row.split(",")
        assert len(columns) == 4, f"Row {idx} should have 4 columns but has {len(columns)}."
        service, port, protocol, approved = columns

        # Port must be an integer string
        assert port.isdigit(), f"Row {idx}: port value {port!r} is not numeric."

        # Protocol must be 'tcp' per the sample data
        assert (
            protocol == "tcp"
        ), f"Row {idx}: protocol value {protocol!r} is not 'tcp' as expected."

        # Approved must be 'yes' or 'no'
        assert approved in {
            "yes",
            "no",
        }, f"Row {idx}: approved value {approved!r} is not 'yes' or 'no'."