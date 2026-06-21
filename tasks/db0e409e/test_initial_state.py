# test_initial_state.py
#
# Pytest suite that validates the **initial** state of the operating
# system / filesystem for the “binary–artifact manager” assignment.
#
# Only the Python standard library and pytest are used.

import os
import re
import stat
import subprocess
from pathlib import Path

import pytest

HOME = Path("/home/user").expanduser()

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _assert_executable(path: Path):
    """
    Assert that `path` exists, is a file and is owner-executable.
    """
    assert path.exists(), f"Expected script missing: {path}"
    assert path.is_file(), f"{path} exists but is not a regular file"
    st_mode = path.stat().st_mode
    # Owner executable bit must be set.
    assert (
        st_mode & stat.S_IXUSR
    ), f"{path} is not executable (owner execute bit is missing)"


def _read_first_line(path: Path) -> str:
    with path.open("r", encoding="utf-8") as f:
        first = f.readline().rstrip("\n")
    return first


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_required_directories_exist_and_writable():
    """
    Required directories must exist (exact absolute paths) and be writable
    by the current user.  They do **not** have to be world-writable.
    """

    required_dirs = [
        HOME / "artifacts",
        HOME / "artifacts" / "releases",
        HOME / "artifacts" / "snapshots",
        HOME / "artifacts" / "thirdparty",
        HOME / "bin",
        HOME / "logs",
    ]

    for d in required_dirs:
        assert d.exists(), f"Missing required directory: {d}"
        assert d.is_dir(), f"{d} exists but is not a directory"
        # Write permission check
        assert os.access(
            d, os.W_OK
        ), f"Directory {d} is not writable by the current user"


def test_cleanup_script_properties():
    """
    /home/user/bin/cleanup_artifacts.sh must:
      • exist and be executable
      • start with '#!/bin/bash'
      • contain the string 'artifact_cleanup.log'
    """
    script = HOME / "bin" / "cleanup_artifacts.sh"
    _assert_executable(script)

    first_line = _read_first_line(script)
    assert (
        first_line == "#!/bin/bash"
    ), f"The first line of {script} must be '#!/bin/bash' (found: {first_line!r})"

    with script.open("r", encoding="utf-8") as f:
        body = f.read()

    assert (
        "artifact_cleanup.log" in body
    ), f"{script} does not reference 'artifact_cleanup.log'"


def test_rotation_script_properties():
    """
    /home/user/bin/rotate_cleanup_log.sh must:
      • exist and be executable
      • start with '#!/bin/bash'
      • contain the string 'rotation_audit.log'
    """
    script = HOME / "bin" / "rotate_cleanup_log.sh"
    _assert_executable(script)

    first_line = _read_first_line(script)
    assert (
        first_line == "#!/bin/bash"
    ), f"The first line of {script} must be '#!/bin/bash' (found: {first_line!r})"

    with script.open("r", encoding="utf-8") as f:
        body = f.read()

    assert (
        "rotation_audit.log" in body
    ), f"{script} does not reference 'rotation_audit.log'"


def test_artifact_cleanup_log_initial_content():
    """
    /home/user/logs/artifact_cleanup.log must contain exactly one line
    that matches the required summary-only regex.
    """
    log_file = HOME / "logs" / "artifact_cleanup.log"
    assert log_file.exists(), "artifact_cleanup.log does not exist"
    assert log_file.is_file(), "artifact_cleanup.log is not a regular file"

    with log_file.open("r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]

    assert len(lines) == 1, (
        "artifact_cleanup.log must contain exactly ONE line at this stage "
        f"(found {len(lines)})"
    )

    summary_regex = re.compile(
        r"^[0-9]{4}-[0-9]{2}-[0-9]{2} "
        r"[0-9]{2}:[0-9]{2}:[0-9]{2} - summary: deleted 0 files occupying 0 bytes$"
    )
    assert summary_regex.match(
        lines[0]
    ), "The single line in artifact_cleanup.log does not match the required format"


def _get_user_crontab() -> list[str]:
    """
    Returns the current user's crontab as a list of non-empty,
    non-comment lines (stripped).
    """
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        assert (
            exc.returncode == 1
        ), "Failed to read crontab (crontab -l). Ensure a user crontab exists."
        # If exit status 1: usually means no crontab for user.
        return []

    lines = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    return lines


def test_crontab_contains_exactly_two_required_entries():
    """
    The user crontab must contain ONLY the two required lines,
    nothing more, nothing less, formatting exactly as prescribed.
    """
    expected_lines = [
        "17 3 * * * /home/user/bin/cleanup_artifacts.sh 45",
        "10 4 * * 0 /home/user/bin/rotate_cleanup_log.sh",
    ]

    actual_lines = _get_user_crontab()

    # Fail fast if counts mismatch so the message is helpful
    assert (
        len(actual_lines) == len(expected_lines)
    ), f"Crontab must contain exactly {len(expected_lines)} non-comment entries (found {len(actual_lines)}). Actual lines: {actual_lines}"

    # Compare line by line in order (order is not mandated by cron but we
    # keep the requirement strict as per spec.)
    mismatches = [
        (i, exp, act)
        for i, (exp, act) in enumerate(zip(expected_lines, actual_lines), start=1)
        if exp != act
    ]
    assert (
        not mismatches
    ), f"Crontab entries do not match the required lines: {mismatches}"