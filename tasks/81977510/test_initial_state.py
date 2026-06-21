# test_initial_state.py
#
# This pytest suite validates that the container is in the **expected
# initial state _before_ the student carries out the benchmark task.**
#
# What we check
# -------------
# 1. The benchmark target script `/home/user/scripts/sleep_for.py`
#    • Exists, is a file, and is executable.
#    • Contains the exact reference implementation lines.
# 2. GNU time is available at `/usr/bin/time` and understands `-f %e`.
# 3. GNU parallel is installed and discoverable via `shutil.which`.
#
# NOTE:
# • We deliberately **do not** test for the presence or absence of any
#   output artefacts such as `/home/user/benchmarks` or the CSV file,
#   because those are part of the student’s deliverable.
# • Only stdlib and pytest are used.

import os
import re
import stat
import subprocess
import sys
from pathlib import Path

import pytest


SLEEP_SCRIPT = Path("/home/user/scripts/sleep_for.py")
GNU_TIME = Path("/usr/bin/time")


# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def _is_executable(path: Path) -> bool:
    """Return True if the given path has the executable bit for the owner."""
    mode = path.stat().st_mode
    return bool(mode & stat.S_IXUSR)


# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_sleep_script_exists_and_is_executable():
    assert SLEEP_SCRIPT.is_file(), (
        f"Expected the benchmark script at '{SLEEP_SCRIPT}', "
        "but it is missing or not a regular file."
    )
    assert _is_executable(SLEEP_SCRIPT), (
        f"Script '{SLEEP_SCRIPT}' exists but is not marked executable."
    )


def test_sleep_script_contents_are_correct():
    expected_lines = [
        "import sys, time",
        "if __name__ == \"__main__\":",
        "    secs = int(sys.argv[1]) if len(sys.argv) > 1 else 0",
        "    time.sleep(secs)",
    ]
    contents = SLEEP_SCRIPT.read_text().splitlines()
    # We assert that ALL expected lines appear in order, but allow for
    # possible leading `#!/usr/bin/env python` shebangs or trailing newlines.
    last_found_idx = -1
    for line in expected_lines:
        try:
            idx = contents.index(line, last_found_idx + 1)
        except ValueError:  # pragma: no cover
            pytest.fail(
                f"Line '{line}' not found in {SLEEP_SCRIPT}; the script does "
                "not match the expected reference implementation."
            )
        last_found_idx = idx


def test_gnu_time_exists_and_supports_format_option(tmp_path):
    assert GNU_TIME.is_file(), (
        f"GNU time expected at '{GNU_TIME}' but the file is missing."
    )

    # The quickest reliable command we can time is `true` (a builtin in many
    # shells).  We invoke `/usr/bin/env` python -c 'pass' to avoid shell.
    cmd = [
        str(GNU_TIME),
        "-f",
        "%e",
        sys.executable,
        "-c",
        "pass",
    ]
    # We redirect stderr -> stdout to capture the elapsed time easily.
    result = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=True
    )

    # GNU time should print *only* the elapsed seconds followed by a newline.
    output = result.stdout.strip()
    assert re.fullmatch(r"[0-9]+\.[0-9]+", output), (
        "GNU time does not appear to recognise the '-f %e' format specifier. "
        f"Command output was: '{output}'"
    )


def test_gnu_parallel_is_available():
    import shutil

    parallel_path = shutil.which("parallel")
    assert parallel_path, "GNU parallel is not installed or not found in PATH."
    assert Path(parallel_path).is_file(), (
        f"GNU parallel was reported at '{parallel_path}' but the path is invalid."
    )


def test_sleep_script_executes_correctly_short_run(tmp_path):
    """
    Sanity-check that running the sleep script with argument '1'
    actually sleeps for (approximately) one second and exits with 0.
    We allow up to 2 s real time to accommodate CI variance.
    """
    import time

    start = time.time()
    result = subprocess.run(
        [sys.executable, str(SLEEP_SCRIPT), "1"], check=True
    )
    elapsed = time.time() - start
    assert result.returncode == 0, "sleep_for.py did not exit cleanly (code ≠ 0)."
    assert 1.0 <= elapsed <= 2.5, (
        f"sleep_for.py was expected to sleep ~1 s; actual elapsed time was {elapsed:.2f}s."
    )