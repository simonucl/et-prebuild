# test_initial_state.py
#
# This pytest-suite validates the machine *before* the student runs the
# benchmarking task.  It checks that the reference data, directories and
# required tools are present, while the deliverable log-file is *not* yet
# created.

import os
import subprocess
import stat
import re
import pytest
from pathlib import Path

HOME = Path("/home/user")
DATA_DIR = HOME / "benchmark_data"
BENCHMARK_DIR = HOME / "benchmarks"
SMALL_DATA = DATA_DIR / "small.txt"
LARGE_DATA = DATA_DIR / "large.txt"
DELIVERABLE = BENCHMARK_DIR / "update_benchmark.log"


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------
def _is_executable(path: Path) -> bool:
    "True if the given path exists and has any executable bit set."
    return path.exists() and path.is_file() and bool(path.stat().st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH))


def _run(cmd):
    "Run *cmd* (list) and return CompletedProcess, raising on failure to start."
    return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
def test_required_directories_exist():
    missing = [p for p in (DATA_DIR, BENCHMARK_DIR) if not p.is_dir()]
    assert not missing, (
        "The following required directories are missing:\n  " + "\n  ".join(map(str, missing))
    )


@pytest.mark.parametrize("file_path", [SMALL_DATA, LARGE_DATA])
def test_reference_files_exist_and_non_empty(file_path: Path):
    assert file_path.is_file(), f"Reference data file {file_path} is missing."
    size = file_path.stat().st_size
    assert size > 0, f"Reference data file {file_path} is empty (size == 0)."
    # Sanity-check that the file is text containing digits and newlines.
    with file_path.open() as fh:
        sample = fh.read(256)
    assert re.fullmatch(r"[\d\n\r\s]+", sample), (
        f"Reference data file {file_path} does not look like numeric text."
    )


def test_large_is_larger_than_small():
    small_size = SMALL_DATA.stat().st_size
    large_size = LARGE_DATA.stat().st_size
    assert large_size > small_size, (
        f"{LARGE_DATA} (size={large_size}) is not larger than {SMALL_DATA} (size={small_size})."
    )


def test_sort_binary_is_available_and_supports_parallel():
    # 1. Ensure 'sort' is invocable.
    proc = _run(["sort", "--version"])
    assert proc.returncode == 0, "'sort --version' failed; GNU sort may be missing."
    # 2. Confirm that the help mentions '--parallel'.
    help_proc = _run(["sort", "--help"])
    assert help_proc.returncode == 0, "'sort --help' failed."
    assert "--parallel" in help_proc.stdout or "--parallel" in help_proc.stderr, (
        "The installed 'sort' does not advertise the '--parallel' option; "
        "updated GNU coreutils may not be installed."
    )
    # 3. Smoke-test the option to make sure it is accepted.
    smoke = _run(
        ["sort", "--parallel=4", str(SMALL_DATA)]
    )
    assert smoke.returncode == 0, (
        "'sort --parallel=4' exited with non-zero status "
        f"{smoke.returncode}. stderr:\n{smoke.stderr}"
    )


def test_usr_bin_time_exists_and_executable():
    time_path = Path("/usr/bin/time")
    assert _is_executable(time_path), (
        f"{time_path} is missing or not executable. "
        "The benchmark must use '/usr/bin/time -f %E' or '-f %e'."
    )


def test_deliverable_not_present_yet():
    assert not DELIVERABLE.exists(), (
        f"The deliverable log-file {DELIVERABLE} already exists. "
        "The initial state should *not* contain the benchmark results."
    )