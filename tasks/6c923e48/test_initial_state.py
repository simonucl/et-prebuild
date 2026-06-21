# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state that must be
# present before the student carries out the task.  It deliberately
# avoids looking for – or mentioning – any artefacts that the student
# is expected to create.

from pathlib import Path

import pytest


BACKUP_DIR = Path("/home/user/backup")

OLD_REPORT = BACKUP_DIR / "disk_usage_report_old.txt"
NEW_REPORT = BACKUP_DIR / "disk_usage_report_new.txt"

OLD_EXPECTED_LINES = [
    "Filesystem      Size  Used Avail Use% Mounted on\n",
    "/dev/sda1       40G   30G  8G   79% /\n",
    "/dev/sdb1       100G  60G  35G  65% /data\n",
    "tmpfs           2.0G  0    2.0G  0% /dev/shm\n",
]

NEW_EXPECTED_LINES = [
    "Filesystem      Size  Used Avail Use% Mounted on\n",
    "/dev/sda1       40G   28G  10G  72% /\n",
    "/dev/sdb1       100G  55G  40G  60% /data\n",
    "tmpfs           2.0G  0    2.0G  0% /dev/shm\n",
]


def _read_file(path: Path):
    """Return the list of lines in *path*, failing with a helpful
    message if the file cannot be read."""
    try:
        return path.read_text(encoding="utf-8").splitlines(keepends=True)
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Expected file not found: {path}")
    except PermissionError:  # pragma: no cover
        pytest.fail(f"File exists but cannot be read (permission denied): {path}")


@pytest.mark.parametrize(
    "path, expected_lines",
    [
        (OLD_REPORT, OLD_EXPECTED_LINES),
        (NEW_REPORT, NEW_EXPECTED_LINES),
    ],
)
def test_report_files_exist_with_correct_contents(path: Path, expected_lines):
    # 1. Assert that the path exists and is a regular file
    assert path.exists(), f"Required file is missing: {path}"
    assert path.is_file(), f"Expected a regular file at {path}, but something else exists."

    # 2. Assert that the file contents are exactly as specified
    actual_lines = _read_file(path)

    assert (
        actual_lines == expected_lines
    ), (
        f"File {path} does not contain the expected contents.\n"
        f"Expected ({len(expected_lines)} lines):\n{''.join(expected_lines)}\n"
        f"Found ({len(actual_lines)} lines):\n{''.join(actual_lines)}"
    )