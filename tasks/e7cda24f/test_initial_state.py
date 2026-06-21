# test_initial_state.py
#
# This pytest test-suite verifies that the operating-system / filesystem
# is in the correct initial state *before* the student performs any action.
#
# What is validated:
# 1. The directory /home/user/incoming exists and has permission 0o700.
# 2. The file     /home/user/incoming/artifact_inventory.csv exists,
#    has permission 0o600, and contains the exact nine lines expected
#    (eight data rows plus the header, each terminated with LF).
#
# No tests are performed on any task-output paths (e.g. /home/user/artifact_reports),
# in accordance with the grading spec.

import os
import stat
import pytest

INCOMING_DIR = "/home/user/incoming"
CSV_PATH = "/home/user/incoming/artifact_inventory.csv"

EXPECTED_CSV_LINES = [
    "id,name,repository,sha256,status\n",
    "1,alpha,stable-core,111aaa,approved\n",
    "2,beta,testing-core,222bbb,rejected\n",
    "3,gamma,stable-core,333ccc,approved\n",
    "4,delta,stable-utils,444ddd,approved\n",
    "5,epsilon,stable-core,555eee,pending\n",
    "6,zeta,experimental,666fff,approved\n",
    "7,eta,stable-utils,777ggg,rejected\n",
    "8,theta,stable-core,888hhh,approved\n",
]


def _mode(path):
    "Return the permission bits of a filesystem object, e.g. 0o755."
    return stat.S_IMODE(os.stat(path).st_mode)


def test_incoming_directory_exists_and_permissions():
    assert os.path.isdir(INCOMING_DIR), (
        f"Required directory {INCOMING_DIR!r} is missing."
    )

    expected_mode = 0o700
    actual_mode = _mode(INCOMING_DIR)
    assert actual_mode == expected_mode, (
        f"Directory {INCOMING_DIR!r} must have permissions {oct(expected_mode)}, "
        f"but is {oct(actual_mode)}."
    )


def test_csv_file_exists_and_permissions():
    assert os.path.isfile(CSV_PATH), (
        f"Required CSV file {CSV_PATH!r} is missing."
    )

    expected_mode = 0o600
    actual_mode = _mode(CSV_PATH)
    assert actual_mode == expected_mode, (
        f"CSV file {CSV_PATH!r} must have permissions {oct(expected_mode)}, "
        f"but is {oct(actual_mode)}."
    )


def test_csv_content_exact():
    try:
        with open(CSV_PATH, "r", encoding="utf-8", newline="") as f:
            lines = f.readlines()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {CSV_PATH!r}: {exc}")

    assert lines == EXPECTED_CSV_LINES, (
        f"CSV file {CSV_PATH!r} does not contain the expected contents.\n"
        f"Expected {len(EXPECTED_CSV_LINES)} lines:\n{''.join(EXPECTED_CSV_LINES)}\n"
        f"Found {len(lines)} lines:\n{''.join(lines)}"
    )