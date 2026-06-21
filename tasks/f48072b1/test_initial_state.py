# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem state
# *before* the student performs any action for the “backup-integrity
# engineer” task.
#
# The tests assert that:
#   • The three expected backup-log files exist at their absolute paths.
#   • Each log file’s byte-for-byte contents exactly match the truth-value
#     specification (including the terminating newline).
#   • No additional daily backup directories are present.
#   • The /home/user/backup_audit directory (and its artefacts) do *not*
#     exist yet.
#   • The checksum-error counts derived from the logs equal the declared
#     ground truth: overall 3 errors; 1 on 2023-08-01, 2 on 2023-08-02,
#     and 0 on 2023-08-03.
#
# Only stdlib + pytest are used.

import re
from pathlib import Path
import pytest

HOME = Path("/home/user")
BACKUPS_DIR = HOME / "backups"

EXPECTED_DAILIES = {
    "2023-08-01": "backup_20230801.log",
    "2023-08-02": "backup_20230802.log",
    "2023-08-03": "backup_20230803.log",
}

# Truth-value contents (each string terminates with \n).
EXPECTED_CONTENTS = {
    "2023-08-01": (
        "2023-08-01 00:59:59 INFO Starting backup\n"
        "2023-08-01 01:15:42 ERROR db01.tar.gz checksum mismatch\n"
        "2023-08-01 01:22:10 INFO db01.tar.gz uploaded\n"
        "2023-08-01 01:30:00 INFO Backup finished\n"
    ),
    "2023-08-02": (
        "2023-08-02 00:59:58 INFO Starting backup\n"
        "2023-08-02 01:12:02 ERROR web_assets.zip checksum mismatch\n"
        "2023-08-02 01:12:03 WARN Retrying web_assets.zip upload\n"
        "2023-08-02 01:44:22 ERROR db02.tar.gz checksum mismatch\n"
        "2023-08-02 02:01:00 INFO Backup finished\n"
    ),
    "2023-08-03": (
        "2023-08-03 01:00:01 INFO Starting backup\n"
        "2023-08-03 01:33:47 INFO No errors detected\n"
        "2023-08-03 02:00:00 INFO Backup finished\n"
    ),
}

CHECKSUM_REGEX = re.compile(
    r"^20[0-9]{2}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} ERROR .* checksum mismatch$"
)


def test_daily_directories_exist_and_nothing_more():
    """
    Ensure that /home/user/backups contains exactly the three expected
    daily directories and no others.
    """
    assert BACKUPS_DIR.is_dir(), f"Expected directory {BACKUPS_DIR} is missing"

    daily_dirs = sorted(p.name for p in BACKUPS_DIR.iterdir() if p.is_dir())
    expected_dirs = sorted(EXPECTED_DAILIES.keys())

    assert daily_dirs == expected_dirs, (
        "Mismatch in daily backup directories.\n"
        f"Expected: {expected_dirs}\n"
        f"Found   : {daily_dirs}"
    )


@pytest.mark.parametrize("day,filename", EXPECTED_DAILIES.items())
def test_each_log_file_exists(day, filename):
    """
    Verify the presence of each backup log file.
    """
    log_path = BACKUPS_DIR / day / filename
    assert log_path.is_file(), f"Expected log file {log_path} is missing"


@pytest.mark.parametrize("day,expected_text", EXPECTED_CONTENTS.items())
def test_log_file_contents_exact(day, expected_text):
    """
    Confirm each log file matches the exact truth-value contents byte-for-byte.
    """
    filename = EXPECTED_DAILIES[day]
    log_path = BACKUPS_DIR / day / filename

    actual_text = log_path.read_text(encoding="utf-8")
    assert (
        actual_text == expected_text
    ), f"Contents of {log_path} do not match expected truth value."


def _collect_checksum_error_lines():
    """
    Helper: iterate over all *.log files and collect lines matching the
    checksum-mismatch regex. Returns a tuple (all_lines, per_day_counts)
    where:
        all_lines         – list with global chronological ordering
        per_day_counts    – dict { 'YYYY-MM-DD': int, ... }
    """
    all_lines = []
    per_day_counts = {day: 0 for day in EXPECTED_DAILIES}

    # Process days in chronological order.
    for day in sorted(EXPECTED_DAILIES):
        log_path = BACKUPS_DIR / day / EXPECTED_DAILIES[day]
        with log_path.open(encoding="utf-8") as fh:
            for line in fh:
                line = line.rstrip("\n")
                if CHECKSUM_REGEX.match(line):
                    all_lines.append(line)
                    per_day_counts[day] += 1

    return all_lines, per_day_counts


def test_checksum_error_statistics_match_truth():
    """
    The log files should yield exactly:
        • 3 checksum-error lines total
        • Per-day counts: 1, 2, 0 (for 1st, 2nd, 3rd Aug respectively)
    """
    all_lines, per_day_counts = _collect_checksum_error_lines()

    # Overall total
    assert len(all_lines) == 3, (
        "Expected exactly 3 checksum-error lines across all logs, "
        f"but found {len(all_lines)}"
    )

    # Per-day counts
    expected_counts = {"2023-08-01": 1, "2023-08-02": 2, "2023-08-03": 0}
    assert (
        per_day_counts == expected_counts
    ), f"Per-day checksum-error counts mismatch.\nExpected: {expected_counts}\nFound   : {per_day_counts}"


def test_backup_audit_directory_absent_initially():
    """
    The student must create /home/user/backup_audit during their work; it
    should NOT exist before they start.
    """
    audit_dir = HOME / "backup_audit"

    assert not audit_dir.exists(), (
        f"Directory {audit_dir} should not exist at the start of the exercise. "
        "It must be created by the student."
    )