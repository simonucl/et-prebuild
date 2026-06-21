# test_initial_state.py
#
# Pytest suite that validates the initial state of the operating-system /
# filesystem *before* the student performs any action on the task
# “distributed time-out analysis”.
#
# What we verify:
#   1. /home/user/distributed_logs            … directory must exist
#   2. The three log files below              … must exist, be readable,
#                                               and contain the EXACT
#                                               lines stated in the task
#      ├─ serviceA.log
#      ├─ serviceB.log
#      └─ serviceC.log
#   3. /home/user/analysis                    … must either NOT exist,
#                                               or exist but be COMPLETELY
#                                               empty (no artefacts yet)
#
# Any deviation causes a clear pytest failure that tells the learner
# exactly what is missing or differs from the expected truth.
#
# Only stdlib + pytest are used.

from pathlib import Path
import stat
import pytest

LOG_DIR = Path("/home/user/distributed_logs")
ANALYSIS_DIR = Path("/home/user/analysis")

EXPECTED_CONTENT = {
    "serviceA.log": [
        '2023-10-18T02:12:00Z SERVICE_A INFO  Node=alpha   Msg="Heartbeat"',
        '2023-10-18T02:13:45Z SERVICE_A ERROR Node=alpha   Msg="Timeout while contacting Node beta"',
        '2023-10-18T02:14:30Z SERVICE_A INFO  Node=alpha   Msg="Recovered connection"',
        '2023-10-18T02:15:01Z SERVICE_A ERROR Node=alpha   Msg="Timeout while contacting Node gamma"',
        '2023-10-18T02:16:30Z SERVICE_A WARN  Node=alpha   Msg="High latency detected"',
        '2023-10-17T23:59:59Z SERVICE_A ERROR Node=alpha   Msg="Timeout while contacting Node delta"',
    ],
    "serviceB.log": [
        '2023-10-18T02:13:00Z SERVICE_B INFO  Node=bravo   Msg="Heartbeat"',
        '2023-10-18T02:14:00Z SERVICE_B ERROR Node=bravo   Msg="Timeout while contacting Node delta"',
        '2023-10-18T02:15:30Z SERVICE_B INFO  Node=bravo   Msg="Recovered connection"',
        '2023-10-18T02:16:17Z SERVICE_B ERROR Node=bravo   Msg="Timeout while contacting Node epsilon"',
    ],
    "serviceC.log": [
        '2023-10-18T02:14:30Z SERVICE_C ERROR Node=charlie Msg="Timeout while contacting Node alpha"',
    ],
}


def _read_file_lines(path: Path):
    """
    Helper that returns a list of *logical* lines for a UTF-8 text file
    without any trailing CR/LF characters.  This is robust against the
    presence or absence of a final newline.
    """
    text = path.read_text(encoding="utf-8")
    # Splitlines() removes the newline characters transparently
    return text.splitlines()


@pytest.mark.dependency(name="log_dir")
def test_distributed_logs_dir_exists():
    assert LOG_DIR.exists(), f"Required directory {LOG_DIR} is missing."
    assert LOG_DIR.is_dir(), f"{LOG_DIR} exists but is not a directory."


@pytest.mark.dependency(depends=["log_dir"], name="log_files")
@pytest.mark.parametrize("fname", sorted(EXPECTED_CONTENT.keys()))
def test_each_log_file_exists_and_readable(fname):
    path = LOG_DIR / fname
    assert path.exists(), f"Expected log file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    mode = path.stat().st_mode
    assert mode & stat.S_IRUSR, f"Log file {path} is not readable by user."


@pytest.mark.dependency(depends=["log_files"])
@pytest.mark.parametrize("fname,expected_lines", EXPECTED_CONTENT.items())
def test_log_file_contents_exact(fname, expected_lines):
    """
    The task supplies the exact ground-truth contents of each log file.
    We verify that the current filesystem matches *verbatim* so the
    exercise starts from a known state.
    """
    path = LOG_DIR / fname
    actual_lines = _read_file_lines(path)

    # Use == so that order, spelling, and number of lines must match.
    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {path} do not match the expected initial state.\n"
        f"Expected ({len(expected_lines)} lines):\n"
        + "\n".join(expected_lines)
        + "\n\nActual ({len(actual_lines)} lines):\n"
        + "\n".join(actual_lines)
    )


def test_analysis_dir_is_absent_or_empty():
    """
    Before the student starts work, /home/user/analysis must *not*
    contain any artefacts.  The directory may be missing entirely, or
    present but completely empty.
    """
    if not ANALYSIS_DIR.exists():
        # Perfectly fine: learner will create it.
        return

    assert ANALYSIS_DIR.is_dir(), f"{ANALYSIS_DIR} exists but is not a directory."

    leftover_items = [p.name for p in ANALYSIS_DIR.iterdir()]
    assert (
        not leftover_items
    ), (
        f"{ANALYSIS_DIR} is expected to be empty before the task begins, "
        f"but contains: {', '.join(leftover_items)}"
    )