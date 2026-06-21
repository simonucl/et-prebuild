# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system
# _before_ the student performs any action for the “capacity-planner” task.
#
# It purposefully FAILS if:
#   • any expected file / directory is missing
#   • the content of critical files does not match the specification
#   • artefacts that should **not** exist yet are already present
#
# Only modules from the Python standard library and pytest are used.

import os
import csv
import math
import pytest
from pathlib import Path

# ---------- Constants ---------------------------------------------------------------------------

HOME = Path("/home/user")
PROJECT_ROOT = HOME / "projects" / "capacity-planner"

VERSION_FILE = PROJECT_ROOT / "VERSION"
CHANGELOG_FILE = PROJECT_ROOT / "CHANGELOG.md"
USAGE_LOG = PROJECT_ROOT / "data" / "usage.log"
RELEASE_NOTES_DIR = PROJECT_ROOT / "release_notes"
TARGET_RELEASE_NOTE = RELEASE_NOTES_DIR / "1.5.0.txt"

EXPECTED_VERSION_CONTENT = "1.4.2\n"
EXPECTED_CHANGELOG_SNIPPET = "## [1.4.2] - 2023-08-10"
UNEXPECTED_CHANGELOG_SNIPPET = "## [1.5.0]"
EXPECTED_CAPACITY_STATS = {
    "CPU_AVG": 57.6,
    "CPU_PEAK": 88.1,
    "MEM_AVG": 70.5,
    "MEM_PEAK": 95.4,
}

# ---------- Helper ------------------------------------------------------------------------------


def parse_usage_log(path: Path):
    """
    Parse usage.log and return four floats rounded to one decimal place:
    cpu_avg, cpu_peak, mem_avg, mem_peak
    """
    cpu_values, mem_values = [], []
    with path.open(newline="") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            # Skip completely empty lines if any
            if not row:
                continue
            try:
                _timestamp, cpu_str, mem_str = row
            except ValueError as exc:  # pragma: no cover
                pytest.fail(f"Unexpected CSV format in {USAGE_LOG}: {row!r}\n{exc}")
            try:
                cpu = float(cpu_str)
                mem = float(mem_str)
            except ValueError as exc:  # pragma: no cover
                pytest.fail(f"CPU/MEM values must be numeric in {USAGE_LOG}: {row!r}\n{exc}")
            cpu_values.append(cpu)
            mem_values.append(mem)

    if not cpu_values or not mem_values:  # pragma: no cover
        pytest.fail(f"{USAGE_LOG} appears to be empty or malformed.")

    cpu_avg = round(sum(cpu_values) / len(cpu_values), 1)
    mem_avg = round(sum(mem_values) / len(mem_values), 1)
    cpu_peak = round(max(cpu_values), 1)
    mem_peak = round(max(mem_values), 1)
    return cpu_avg, cpu_peak, mem_avg, mem_peak


# ---------- Tests--------------------------------------------------------------------------------


def test_project_directory_structure():
    """Top-level project directory and key sub-paths must exist."""
    assert PROJECT_ROOT.is_dir(), f"Missing project directory: {PROJECT_ROOT}"
    assert (PROJECT_ROOT / "data").is_dir(), "Expected data/ directory is missing."
    assert RELEASE_NOTES_DIR.is_dir(), (
        "release_notes/ directory must exist at the start (empty is OK)."
    )


def test_version_file_initial_state():
    """VERSION must exist and contain exactly '1.4.2\\n'."""
    assert VERSION_FILE.is_file(), f"VERSION file not found at {VERSION_FILE}"
    content = VERSION_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_VERSION_CONTENT
    ), f"VERSION file content mismatch.\nExpected: {EXPECTED_VERSION_CONTENT!r}\nFound:    {content!r}"


def test_changelog_contains_previous_entry_and_no_new_entry():
    """
    CHANGELOG.md must already contain the 1.4.2 entry and must *not*
    yet contain any 1.5.0 entry.
    """
    assert CHANGELOG_FILE.is_file(), f"CHANGELOG.md not found at {CHANGELOG_FILE}"
    text = CHANGELOG_FILE.read_text(encoding="utf-8")

    assert (
        "# Changelog" in text
    ), "CHANGELOG.md must start with a '# Changelog' top-level heading."
    assert (
        EXPECTED_CHANGELOG_SNIPPET in text
    ), f"Expected previous entry '{EXPECTED_CHANGELOG_SNIPPET}' not found in CHANGELOG.md."
    assert (
        UNEXPECTED_CHANGELOG_SNIPPET not in text
    ), f"CHANGELOG.md already contains '{UNEXPECTED_CHANGELOG_SNIPPET}', but it should only be added later."


def test_usage_log_values_match_expected():
    """
    The numeric statistics derived from data/usage.log must match the
    expected values provided in the task description.
    """
    assert USAGE_LOG.is_file(), f"usage.log not found at {USAGE_LOG}"
    cpu_avg, cpu_peak, mem_avg, mem_peak = parse_usage_log(USAGE_LOG)

    assert math.isclose(cpu_avg, EXPECTED_CAPACITY_STATS["CPU_AVG"]), (
        f"CPU_AVG mismatch: expected {EXPECTED_CAPACITY_STATS['CPU_AVG']}, got {cpu_avg}"
    )
    assert math.isclose(cpu_peak, EXPECTED_CAPACITY_STATS["CPU_PEAK"]), (
        f"CPU_PEAK mismatch: expected {EXPECTED_CAPACITY_STATS['CPU_PEAK']}, got {cpu_peak}"
    )
    assert math.isclose(mem_avg, EXPECTED_CAPACITY_STATS["MEM_AVG"]), (
        f"MEM_AVG mismatch: expected {EXPECTED_CAPACITY_STATS['MEM_AVG']}, got {mem_avg}"
    )
    assert math.isclose(mem_peak, EXPECTED_CAPACITY_STATS["MEM_PEAK"]), (
        f"MEM_PEAK mismatch: expected {EXPECTED_CAPACITY_STATS['MEM_PEAK']}, got {mem_peak}"
    )


def test_target_release_note_does_not_exist_yet():
    """The 1.5.0 release note file must NOT exist before the student creates it."""
    assert (
        not TARGET_RELEASE_NOTE.exists()
    ), f"{TARGET_RELEASE_NOTE} already exists, but it should only be created after the task is completed."