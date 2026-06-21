# test_initial_state.py
#
# This pytest suite asserts that the *initial* operating-system state
# contains the expected raw log inputs and nothing crucial is missing
# before the student begins the task.  Any failure pin-points exactly
# what is absent or malformed.
#
# Rules honoured:
#   • Only stdlib + pytest are used.
#   • Absolute paths are checked.
#   • No assertion touches the output / audit artefacts.

import os
import csv
import pytest

RAW_DIR = "/home/user/compliance/raw_logs"
LOGIN_CSV = os.path.join(RAW_DIR, "login_events.csv")
FILE_ACCESS_CSV = os.path.join(RAW_DIR, "file_access.csv")


def _read_csv(path):
    """Return rows from CSV file located at *path*."""
    with open(path, encoding="utf-8", newline="") as fp:
        return list(csv.reader(fp))


def test_raw_logs_directory_exists_and_is_directory():
    assert os.path.exists(RAW_DIR), (
        "Directory %s is missing. The initial fixture *must* ship with the "
        "raw log directory in place." % RAW_DIR
    )
    assert os.path.isdir(RAW_DIR), (
        "%s exists but is not a directory; expected a directory that holds the "
        "raw CSV files." % RAW_DIR
    )


@pytest.mark.parametrize(
    "path",
    [LOGIN_CSV, FILE_ACCESS_CSV],
    ids=["login_events.csv presence", "file_access.csv presence"],
)
def test_required_csv_files_exist(path):
    assert os.path.exists(path), (
        "Required input file %s is missing.  It must be present before the "
        "student starts their solution." % path
    )
    assert os.path.isfile(path), (
        "%s exists but is not a regular file. Expected a normal CSV file."
        % path
    )


def test_login_events_csv_content_exact_match():
    expected_rows = [
        ["event_id", "timestamp", "user", "action", "source_ip"],
        ["LE1", "2023-04-01T09:15:27Z", "alice", "login", "192.168.1.10"],
        ["LE2", "2023-04-01T12:47:03Z", "bob", "login", "192.168.1.11"],
        ["LE3", "2023-04-01T17:05:44Z", "alice", "logout", "192.168.1.10"],
        ["LE4", "2023-04-02T08:01:09Z", "charlie", "login", "192.168.1.12"],
        ["LE5", "2023-04-02T11:30:17Z", "bob", "logout", "192.168.1.11"],
    ]

    actual_rows = _read_csv(LOGIN_CSV)
    assert actual_rows == expected_rows, (
        f"{LOGIN_CSV} does not contain the expected rows.\n"
        f"Expected:\n{expected_rows}\n"
        f"Got:\n{actual_rows}"
    )


def test_file_access_csv_content_exact_match():
    expected_rows = [
        ["event_id", "timestamp", "user", "file_path", "operation"],
        ["FA1", "2023-04-01T10:03:12Z", "alice", "/srv/docs/confidential.pdf", "read"],
        ["FA2", "2023-04-01T10:15:55Z", "alice", "/srv/docs/confidential.pdf", "write"],
        ["FA3", "2023-04-01T13:22:40Z", "bob", "/srv/spreadsheets/budget.xlsx", "read"],
        ["FA4", "2023-04-02T09:12:06Z", "charlie", "/srv/scripts/deploy.sh", "read"],
        ["FA5", "2023-04-02T09:45:55Z", "charlie", "/srv/scripts/deploy.sh", "write"],
        ["FA6", "2023-04-02T12:11:33Z", "bob", "/srv/spreadsheets/budget.xlsx", "write"],
    ]

    actual_rows = _read_csv(FILE_ACCESS_CSV)
    assert actual_rows == expected_rows, (
        f"{FILE_ACCESS_CSV} does not contain the expected rows.\n"
        f"Expected:\n{expected_rows}\n"
        f"Got:\n{actual_rows}"
    )