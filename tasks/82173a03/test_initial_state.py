# test_initial_state.py
#
# This test-suite validates that the machine has the basic utilities and
# files needed *before* the student performs the assignment.  It purposely
# avoids checking for any of the soon-to-be-created artefacts (such as the
# /home/user/config_state directory or *.log files).  If any of these tests
# fail, the environment itself is incomplete or broken and the assignment
# cannot be completed.

import os
import subprocess
import sys
from pathlib import Path
import shutil

import pytest


HOME = Path("/home/user")


@pytest.mark.parametrize(
    "path, kind",
    [
        (HOME, "directory"),
        (Path("/proc/meminfo"), "file"),
    ],
)
def test_critical_paths_exist(path: Path, kind: str):
    """
    Verify that essential paths exist on the system.

    We do *not* touch any output artefacts that belong to the assignment.
    """
    if kind == "directory":
        assert path.is_dir(), f"Required directory '{path}' is missing."
    elif kind == "file":
        assert path.is_file(), f"Required file '{path}' is missing."
    else:  # pragma: no cover
        pytest.fail(f"Unknown kind specified for path check: {kind}")


@pytest.mark.parametrize("binary", ["hostname", "uname", "df"])
def test_required_binaries_are_in_path(binary: str):
    """
    The assignment relies on a handful of standard Unix utilities.
    Ensure each can be located via the current PATH.
    """
    found = shutil.which(binary)
    assert (
        found is not None and Path(found).is_file()
    ), f"The binary '{binary}' is not found in PATH."


def test_meminfo_contains_memtotal():
    """
    /proc/meminfo must contain a 'MemTotal' line so the student can
    calculate total RAM.
    """
    with open("/proc/meminfo", encoding="utf-8") as fp:
        for line in fp:
            if line.startswith("MemTotal:"):
                break
        else:
            pytest.fail("'MemTotal' entry not found in /proc/meminfo")


def test_df_root_reports_usage():
    """
    Running `df /` should succeed and return exactly one data line that
    contains a '%' used value (e.g. '12%').
    """
    try:
        completed = subprocess.run(
            ["df", "/"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:  # pragma: no cover  # covered by binary test
        pytest.fail("'df' binary is missing, cannot run `df /`")

    lines = completed.stdout.strip().splitlines()
    assert (
        len(lines) >= 2
    ), "Expected at least two lines from `df /` (header + data line)."

    header, data_line, *rest = lines
    used_field = data_line.split()[4] if len(data_line.split()) >= 5 else ""
    assert (
        used_field.endswith("%") and used_field[:-1].isdigit()
    ), f"Could not parse root filesystem usage percentage from `df /` output: {data_line!r}"


def test_system_time_is_accessible():
    """
    Ensure the Python stdlib can obtain the current UTC time.  This is
    a sanity check for the timestamp the student will embed in the filename.
    """
    try:
        import datetime

        datetime.datetime.utcnow()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"datetime.utcnow() failed: {exc}")


def test_python_version_is_new_enough():
    """
    The student may rely on f-strings or other modern Python features.
    Require at least Python 3.6.
    """
    major, minor = sys.version_info[:2]
    assert (
        major == 3 and minor >= 6
    ) or (major > 3), f"Python ≥3.6 is required, found {sys.version.split()[0]}"