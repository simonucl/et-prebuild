# test_initial_state.py
#
# This pytest suite validates the *initial* operating-system / filesystem
# state before the student attempts the exercise.  It asserts that the
# expected diagnostic files are present with the exact byte-for-byte
# contents described in the task and that no output artefacts have been
# generated yet.

from pathlib import Path

import pytest

HOME = Path("/home/user")
DIAG_DIR = HOME / "diag_logs"

# --------------------------------------------------------------------------- #
# Expected diagnostic files and their exact contents                          #
# --------------------------------------------------------------------------- #

CPU_STATS_EXPECTED = (
    "timestamp,cpu_usage\n"
    "2023-08-01T10:00:00Z,17\n"
    "2023-08-01T10:05:00Z,19\n"
    "2023-08-01T10:10:00Z,17\n"
)

MEM_STATS_EXPECTED = (
    "timestamp,mem_total,mem_used,mem_free\n"
    "2023-08-01T10:00:00Z,8000,5600,2400\n"
    "2023-08-01T10:05:00Z,8000,5700,2300\n"
    "2023-08-01T10:10:00Z,8000,5500,2500\n"
)

DISK_STATS_EXPECTED = (
    "timestamp,disk_use_pct\n"
    "2023-08-01T10:00:00Z,50\n"
    "2023-08-01T10:05:00Z,50.8\n"
    "2023-08-01T10:10:00Z,51.2\n"
)


@pytest.fixture(scope="module")
def expected_files():
    """
    Returns a mapping of filename -> expected_content so that individual
    tests can iterate over it.
    """
    return {
        "cpu_stats.txt": CPU_STATS_EXPECTED,
        "mem_stats.txt": MEM_STATS_EXPECTED,
        "disk_stats.txt": DISK_STATS_EXPECTED,
    }


# --------------------------------------------------------------------------- #
# Directory / file existence checks                                           #
# --------------------------------------------------------------------------- #


def test_diag_directory_exists():
    assert DIAG_DIR.exists(), (
        f"The directory {DIAG_DIR} is missing. It must exist with the "
        "three diagnostic files before the exercise begins."
    )
    assert DIAG_DIR.is_dir(), f"{DIAG_DIR} exists but is not a directory."


def test_only_expected_files_present(expected_files):
    present_files = {p.name for p in DIAG_DIR.iterdir() if p.is_file()}
    expected_set = set(expected_files)
    # The summary_report.tsv and generation.log must NOT be present yet
    forbidden = {"summary_report.tsv", "generation.log"}

    # Helpful assertion messages:
    missing = expected_set - present_files
    unexpected = (present_files - expected_set) - forbidden
    forbidden_present = present_files & forbidden

    assert not missing, (
        "The following required diagnostic file(s) are missing from "
        f"{DIAG_DIR}: {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        "Unexpected file(s) found in the diagnostic directory before the "
        f"exercise starts: {', '.join(sorted(unexpected))}"
    )
    assert not forbidden_present, (
        "Output file(s) that should only appear *after* the exercise has been "
        "completed are already present: "
        f"{', '.join(sorted(forbidden_present))}"
    )


# --------------------------------------------------------------------------- #
# Byte-for-byte content checks                                                #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("filename", ["cpu_stats.txt", "mem_stats.txt", "disk_stats.txt"])
def test_file_contents_exact_match(filename, expected_files):
    path = DIAG_DIR / filename
    assert path.exists(), f"Expected diagnostic file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."

    # Read file as text with universal newlines disabled to preserve bytes.
    content = path.read_text(encoding="utf-8")
    expected = expected_files[filename]

    assert content == expected, (
        f"Contents of {path} do not match the expected initial data.\n"
        f"--- Expected (len={len(expected)}) ---\n{expected!r}\n"
        f"--- Found (len={len(content)}) ---\n{content!r}"
    )


# --------------------------------------------------------------------------- #
# Ensure output artefacts are NOT present yet                                 #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "path",
    [
        DIAG_DIR / "summary_report.tsv",
        DIAG_DIR / "generation.log",
    ],
)
def test_output_files_absent(path):
    assert not path.exists(), (
        f"The output file {path} should not exist before the student "
        "executes their solution."
    )