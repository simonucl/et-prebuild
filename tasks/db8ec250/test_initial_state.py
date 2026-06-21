# test_initial_state.py
#
# Pytest suite that validates the operating-system state *before*
# the student’s solution is executed.
#
# IMPORTANT:
# • We only test pre-existing artefacts.  We deliberately avoid looking for
#   anything that the student is expected to create (e.g. the reports
#   directory or the final log file).
# • All checks are against absolute paths.
# • Only stdlib + pytest are used.

import os
import stat
import pwd
import pytest


SNAPSHOT_PATH = "/home/user/data/ps_snapshot.txt"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _read_snapshot_lines():
    """Return the lines of the snapshot file, stripping the trailing newline."""
    with open(SNAPSHOT_PATH, "r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh]


def _file_mode(path):
    """Return the permission bits (e.g. 0o644) of the given path."""
    return stat.S_IMODE(os.stat(path).st_mode)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_snapshot_file_exists():
    """The ps_snapshot.txt file must exist and be a regular file."""
    assert os.path.isfile(
        SNAPSHOT_PATH
    ), f"Missing snapshot file at expected path: {SNAPSHOT_PATH!r}"


def test_snapshot_file_permissions():
    """
    The snapshot file must be world-readable and only user-writable (0644).
    This matters because the student script will be run as an unprivileged user.
    """
    expected_mode = 0o644
    mode = _file_mode(SNAPSHOT_PATH)
    assert (
        mode == expected_mode
    ), (
        f"Incorrect permissions on {SNAPSHOT_PATH!r}. "
        f"Expected {oct(expected_mode)}, found {oct(mode)}."
    )


def test_snapshot_content_header():
    """First line must match the exact header required by the spec."""
    header = _read_snapshot_lines()[0]
    expected = "PID COMMAND %CPU %MEM"
    assert (
        header == expected
    ), f"Snapshot header mismatch. Expected {expected!r}, got {header!r}."


def test_snapshot_has_minimum_process_rows():
    """
    There must be at least five process rows (header + ≥5 data lines = ≥6 lines).
    The student's script needs at least five to build the report.
    """
    lines = _read_snapshot_lines()
    assert (
        len(lines) >= 6
    ), f"Snapshot file should contain header + ≥5 data rows, only found {len(lines)-1} data rows."


@pytest.mark.parametrize("line_no,line", enumerate(_read_snapshot_lines()[1:], start=2))
def test_each_data_line_has_valid_columns(line_no, line):
    """
    Every data line must have exactly four whitespace-separated columns:
    PID (int), COMMAND (str), %CPU (float), %MEM (float)
    """
    parts = line.split()
    assert (
        len(parts) == 4
    ), f"Line {line_no} in snapshot does not have 4 columns: {line!r}"
    pid, command, cpu, mem = parts

    # PID must be an integer > 0
    assert pid.isdigit() and int(pid) > 0, f"Line {line_no}: invalid PID {pid!r}"

    # COMMAND must be non-empty and may not contain whitespace (already ensured)
    assert command, f"Line {line_no}: COMMAND field is empty"

    # %CPU and %MEM must parse as floats
    for field_name, value in (("%CPU", cpu), ("%MEM", mem)):
        try:
            float_val = float(value)
        except ValueError:  # pragma: no cover
            raise AssertionError(
                f"Line {line_no}: {field_name} value {value!r} is not a valid float"
            )
        assert (
            float_val >= 0.0
        ), f"Line {line_no}: {field_name} value {value!r} must be non-negative"