# test_initial_state.py
#
# Pytest suite to verify that the operating-system / filesystem
# is in the correct *initial* state before the student starts
# manipulating data.  It checks that:
#
# 1. The expected seed files exist under /home/user/data/.
# 2. Those seed files contain the exact, line-for-line content
#    described in the specification (including a single final
#    trailing newline).
# 3. The two output files that the student is supposed to create
#    later do *not* exist yet.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path
import pytest

DATA_DIR = Path("/home/user/data")

HOSTS_FILE = DATA_DIR / "hosts.txt"
METRICS_FILE = DATA_DIR / "metrics.txt"

# Files that must *not* exist before the student’s solution runs
HOST_CPU_FILE = DATA_DIR / "host_cpu.csv"
ALERTS_FILE = DATA_DIR / "high_cpu_alerts.log"

EXPECTED_HOSTS_LINES = ["web01\n", "web02\n", "db01\n", "cache01\n"]
EXPECTED_METRICS_LINES = [
    "cpu=23 mem=40\n",
    "cpu=87 mem=66\n",
    "cpu=55 mem=72\n",
    "cpu=92 mem=31\n",
]


def _read_lines(path: Path):
    """Read a file in binary mode then decode as UTF-8.

    This allows us to verify the precise newline usage and ensure
    the file ends with *exactly* one trailing newline.
    """
    with path.open("rb") as fh:
        raw = fh.read()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{path} is not valid UTF-8: {exc}")  # pragma: no cover
    return raw, text.splitlines(keepends=True)


def test_data_directory_exists():
    assert DATA_DIR.is_dir(), (
        f"The data directory {DATA_DIR} does not exist.\n"
        "Create it first and place the seed files inside."
    )


def test_hosts_txt_exists_and_contents():
    assert HOSTS_FILE.is_file(), (
        f"{HOSTS_FILE} is missing.\n"
        "The exercise requires this seed file to be present with four hostnames."
    )

    raw, lines = _read_lines(HOSTS_FILE)

    # Verify final newline (file ends with single '\n')
    assert raw.endswith(b"\n"), (
        f"{HOSTS_FILE} must end with a single newline (\\n)."
    )

    assert lines == EXPECTED_HOSTS_LINES, (
        f"{HOSTS_FILE} does not contain the expected hostnames or "
        "has extra / missing lines.\n"
        f"Expected:\n{''.join(EXPECTED_HOSTS_LINES)!r}\n"
        f"Found:\n{''.join(lines)!r}"
    )


def test_metrics_txt_exists_and_contents():
    assert METRICS_FILE.is_file(), (
        f"{METRICS_FILE} is missing.\n"
        "The exercise requires this seed file to be present with four metrics lines."
    )

    raw, lines = _read_lines(METRICS_FILE)

    # Verify final newline
    assert raw.endswith(b"\n"), (
        f"{METRICS_FILE} must end with a single newline (\\n)."
    )

    assert lines == EXPECTED_METRICS_LINES, (
        f"{METRICS_FILE} does not match the expected metrics data.\n"
        f"Expected:\n{''.join(EXPECTED_METRICS_LINES)!r}\n"
        f"Found:\n{''.join(lines)!r}"
    )


def test_output_files_do_not_yet_exist():
    """The CSV and alert log should not pre-exist before the student runs their solution."""
    assert not HOST_CPU_FILE.exists(), (
        f"{HOST_CPU_FILE} already exists, but it should be created by the student's script—not beforehand."
    )
    assert not ALERTS_FILE.exists(), (
        f"{ALERTS_FILE} already exists, but it should be created by the student's script—not beforehand."
    )