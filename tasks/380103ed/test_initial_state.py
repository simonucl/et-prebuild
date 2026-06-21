# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state before the student performs any action for the “profiling” task.
#
# The tests assert the presence and basic integrity of the resources that
# are guaranteed to exist when the container starts.  They do NOT check
# for any output artefacts that the student is expected to create later
# on (cpu_time_raw.log, io_strace_raw.log, session_summary.log, …).

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
APPS_DIR = HOME / "apps"
PROFILES_DIR = HOME / "profiles"
CPU_STRESS = APPS_DIR / "cpu_stress.py"
IO_STRESS = APPS_DIR / "io_stress.py"


@pytest.mark.parametrize(
    "p, kind",
    [
        (APPS_DIR, "directory"),
        (PROFILES_DIR, "directory"),
        (CPU_STRESS, "file"),
        (IO_STRESS, "file"),
    ],
)
def test_paths_exist(p: Path, kind: str):
    """
    Verify that the critical paths exist and are of the expected type.
    """
    assert p.exists(), f"Expected {kind} {p} to exist, but it does not."
    if kind == "directory":
        assert p.is_dir(), f"Expected {p} to be a directory."
    else:
        assert p.is_file(), f"Expected {p} to be a regular file."


def test_profiles_dir_is_writable():
    """
    The /home/user/profiles directory must be writable so the student can
    create the log files there.
    """
    mode = PROFILES_DIR.stat().st_mode
    is_writable = bool(mode & stat.S_IWUSR)
    assert is_writable, f"{PROFILES_DIR} is not writable by the current user."


def test_cpu_stress_contents():
    """
    Sanity-check that cpu_stress.py still contains the expected signature
    lines; this guards against accidental edits or truncation.
    """
    text = CPU_STRESS.read_text(encoding="utf-8")

    required_snippets = [
        "def busy():",
        "for i in range(5_000_00)",
        "total += math.sqrt(i)",
        'if __name__ == "__main__":',
    ]

    for snippet in required_snippets:
        assert (
            snippet in text
        ), f"{CPU_STRESS} is missing expected snippet: {snippet!r}"


def test_io_stress_contents():
    """
    Sanity-check that io_stress.py still contains the expected signature
    lines.
    """
    text = IO_STRESS.read_text(encoding="utf-8")

    required_snippets = [
        "def thrash():",
        "tempfile.mkstemp()",
        "for i in range(1000):",
        'f.write(b"x" * 4096)',
        'if __name__ == "__main__":',
    ]

    for snippet in required_snippets:
        assert (
            snippet in text
        ), f"{IO_STRESS} is missing expected snippet: {snippet!r}"