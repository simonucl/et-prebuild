# test_initial_state.py
#
# This pytest suite validates that the micro-benchmark sources expected by the
# assignment are present **before** the student performs any actions that create
# logs, summaries, or reports.  It deliberately avoids touching any of the
# output paths (​/home/user/perf_bench/logs, /home/user/perf_bench/summary, …).

import os
import stat
import subprocess
from pathlib import Path

import pytest


APPS_DIR = Path("/home/user/perf_bench/apps")
EXPECTED_APPS = {
    "app_sort.py": "benchmark_result_ms:42",
    "app_math.py": "benchmark_result_ms:84",
}


def _read_mode(path: Path) -> int:
    """Return the file mode bits (permission bits only)."""
    return stat.S_IMODE(path.stat().st_mode)


def _is_executable(mode_bits: int) -> bool:
    """Simple POSIX check: is the file executable by *any* of user/group/other?"""
    return bool(mode_bits & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def test_apps_directory_exists_and_is_directory():
    assert APPS_DIR.exists(), (
        f"Required directory {APPS_DIR} does not exist. "
        "Create it at /home/user/perf_bench/apps."
    )
    assert APPS_DIR.is_dir(), (
        f"{APPS_DIR} exists but is not a directory. "
        "It must be a directory containing the benchmark scripts."
    )


@pytest.mark.parametrize("filename,expected_line", EXPECTED_APPS.items())
def test_benchmark_files_exist_and_are_executable(filename, expected_line):
    app_path = APPS_DIR / filename

    # --- Presence checks ----------------------------------------------------
    assert app_path.exists(), (
        f"Expected benchmark file {app_path} does not exist. "
        "Ensure the file is present with the correct name."
    )
    assert app_path.is_file(), (
        f"{app_path} exists but is not a regular file."
    )

    # --- Executable permission check ----------------------------------------
    mode_bits = _read_mode(app_path)
    assert _is_executable(mode_bits), (
        f"{app_path} is not marked as executable. "
        "Use chmod +x to set the execute bit."
    )

    # --- Content / functional check -----------------------------------------
    completed = subprocess.run(
        [str(app_path)], capture_output=True, text=True, check=True
    )
    stdout = completed.stdout.strip().splitlines()

    assert len(stdout) == 1, (
        f"{app_path} should print exactly one line, "
        f"but printed {len(stdout)} lines."
    )
    assert stdout[0] == expected_line, (
        f"{app_path} printed '{stdout[0]}' but was expected to print "
        f"'{expected_line}'. Do not modify the benchmark script output."
    )