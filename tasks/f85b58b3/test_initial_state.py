# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the filesystem
# before the student starts working on the exercise.  These tests make
# sure that:
#
# • The two source CSV files exist under /home/user/monitoring/logs
#   and contain the exact five lines (1 header + 4 data) described in
#   the task description.
# • The /home/user/monitoring/alerts directory either does not yet
#   exist or, if it does, is completely empty (i.e. the student has not
#   started creating the required output files).
#
# If any check fails, the assertion messages precisely describe what is
# missing or incorrect.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

CPU_STATS = Path("/home/user/monitoring/logs/cpu_stats.csv")
MEM_STATS = Path("/home/user/monitoring/logs/mem_stats.csv")
ALERTS_DIR = Path("/home/user/monitoring/alerts")
ALERT_FEED = ALERTS_DIR / "alert_feed_20230801.txt"
PROCESS_LOG = ALERTS_DIR / "process.log"


def read_lines(path: Path):
    """Return a list of lines without their trailing newline."""
    with path.open("r", encoding="utf-8") as fh:
        return [line.rstrip("\n") for line in fh]


# --------------------------------------------------------------------------- #
# Existence checks                                                            #
# --------------------------------------------------------------------------- #
def test_logs_directory_exists():
    logs_dir = Path("/home/user/monitoring/logs")
    assert logs_dir.is_dir(), (
        f"Expected directory {logs_dir} to exist. "
        "It should already contain the two CSV source files."
    )


def test_cpu_stats_exists():
    assert CPU_STATS.is_file(), (
        f"Missing file: {CPU_STATS}. The exercise starts with this CSV already present."
    )


def test_mem_stats_exists():
    assert MEM_STATS.is_file(), (
        f"Missing file: {MEM_STATS}. The exercise starts with this CSV already present."
    )


# --------------------------------------------------------------------------- #
# CSV content checks                                                          #
# --------------------------------------------------------------------------- #
EXPECTED_CPU_LINES = [
    "timestamp,host,cpu_usage,proc_run",
    "2023-08-01T00:00:00Z,web01,25,120",
    "2023-08-01T00:05:00Z,db01,45,87",
    "2023-08-01T00:10:00Z,web01,27,122",
    "2023-08-01T00:15:00Z,db01,46,90",
]

EXPECTED_MEM_LINES = [
    "timestamp,host,mem_free,swap_used",
    "2023-08-01T00:00:00Z,web01,1024,128",
    "2023-08-01T00:05:00Z,db01,512,256",
    "2023-08-01T00:10:00Z,web01,1000,130",
    "2023-08-01T00:15:00Z,db01,500,260",
]


def _check_csv_content(path: Path, expected_lines: list[str]):
    lines = read_lines(path)
    assert (
        lines == expected_lines
    ), f"Content mismatch in {path}. Expected exactly:\n" + "\n".join(expected_lines)


def _check_four_columns(path: Path):
    for idx, line in enumerate(read_lines(path), start=1):
        cols = line.split(",")
        assert len(cols) == 4, (
            f"File {path} should have exactly 4 comma-separated columns "
            f"per line, but line {idx} has {len(cols)} columns: {line!r}"
        )


def test_cpu_stats_content_and_shape():
    _check_csv_content(CPU_STATS, EXPECTED_CPU_LINES)
    _check_four_columns(CPU_STATS)


def test_mem_stats_content_and_shape():
    _check_csv_content(MEM_STATS, EXPECTED_MEM_LINES)
    _check_four_columns(MEM_STATS)


# --------------------------------------------------------------------------- #
# Alerts directory must be pristine before the exercise begins               #
# --------------------------------------------------------------------------- #
def test_alerts_directory_initial_state():
    """
    Before the learner runs any commands, /home/user/monitoring/alerts
    should NOT contain the target files.  It may not exist at all; if it
    does, it must be empty.
    """
    if not ALERTS_DIR.exists():
        # Perfectly fine: directory not yet created.
        return

    assert ALERTS_DIR.is_dir(), (
        f"{ALERTS_DIR} exists but is not a directory. "
        "Please remove or rename it before starting the exercise."
    )

    contents = list(ALERTS_DIR.iterdir())
    assert contents == [], (
        f"{ALERTS_DIR} should be empty before the task begins, "
        f"but found: {[p.name for p in contents]}"
    )

    # Extra defensive checks in case the directory exists but hidden files linger
    assert not ALERT_FEED.exists(), f"{ALERT_FEED} should not exist yet."
    assert not PROCESS_LOG.exists(), f"{PROCESS_LOG} should not exist yet."