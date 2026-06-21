# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem / operating-system state
# before the student performs any action.  All checks are performed against the
# ground-truth described in the task statement.  If any check fails, the error
# message will tell exactly what is missing or differs from the expected state.

import os
import stat
import textwrap

import pytest

HOME = "/home/user"
CAPACITY_DIR = os.path.join(HOME, "capacity_data")
CSV_PATH = os.path.join(CAPACITY_DIR, "server_usage.csv")
LOG_PATH = os.path.join(CAPACITY_DIR, "usage_summary.log")


@pytest.fixture(scope="session")
def expected_csv_content() -> str:
    """
    The exact, byte-for-byte contents expected for
    /home/user/capacity_data/server_usage.csv **including** the final newline.
    """
    content = textwrap.dedent(
        """\
        server_id,cpu_usage_pct,mem_usage_pct
        s1,45,67
        s1,55,65
        s2,80,70
        s2,60,75
        s3,30,40
        """
    )
    # textwrap.dedent keeps the trailing newline of the triple-quoted string.
    # The task explicitly says the file has a final newline, so we must too.
    return content


def _mode(path: str) -> int:
    """Return only the permission bits (e.g. 0o644) for the given path."""
    return stat.S_IMODE(os.stat(path).st_mode)


def test_directory_exists_and_permissions():
    assert os.path.isdir(CAPACITY_DIR), (
        f"Expected directory {CAPACITY_DIR!r} to exist but it does not."
    )

    expected_mode = 0o755
    actual_mode = _mode(CAPACITY_DIR)
    assert actual_mode == expected_mode, (
        f"Directory {CAPACITY_DIR!r} should have permissions "
        f"{oct(expected_mode)} but has {oct(actual_mode)} instead."
    )


def test_csv_file_exists_and_permissions(expected_csv_content):
    assert os.path.isfile(CSV_PATH), (
        f"Expected CSV file {CSV_PATH!r} to exist but it does not."
    )

    expected_mode = 0o644
    actual_mode = _mode(CSV_PATH)
    assert actual_mode == expected_mode, (
        f"File {CSV_PATH!r} should have permissions "
        f"{oct(expected_mode)} but has {oct(actual_mode)} instead."
    )

    with open(CSV_PATH, "r", encoding="utf-8") as fh:
        contents = fh.read()

    assert contents == expected_csv_content, (
        f"Contents of {CSV_PATH!r} do not match the expected ground-truth.\n"
        "Expected:\n"
        f"{expected_csv_content!r}\n\n"
        "Found:\n"
        f"{contents!r}"
    )


def test_no_log_file_yet():
    assert not os.path.exists(LOG_PATH), (
        f"{LOG_PATH!r} must NOT exist before the student runs their solution."
    )


def test_no_extra_files():
    """
    The directory must contain exactly one entry: server_usage.csv.
    Hidden files or any other artefacts are not allowed at this stage.
    """
    entries = sorted(
        entry.name for entry in os.scandir(CAPACITY_DIR) if entry.is_file()
    )
    assert entries == ["server_usage.csv"], (
        f"The directory {CAPACITY_DIR!r} should contain only "
        f"'server_usage.csv' initially, but found: {entries}"
    )