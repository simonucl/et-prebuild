# test_initial_state.py
#
# Pytest suite that validates the **initial** environment *before*
# the student runs any commands.  It checks that:
#
# 1. The staging directory /home/user/environments/ exists.
# 2. The source file /home/user/environments/test_servers.tsv exists
#    and contains the exact, expected, tab-delimited contents.
# 3. None of the target output files are present yet.
#
# Only stdlib and pytest are used.

import os
from pathlib import Path

import pytest

ENV_DIR = Path("/home/user/environments")
SRC_FILE = ENV_DIR / "test_servers.tsv"

# Files that must **not** exist yet.
OUTPUT_FILES = [
    ENV_DIR / "hosts.list",
    ENV_DIR / "host_ip_map.tsv",
    ENV_DIR / "column_ops.log",
]

# Expected exact contents of test_servers.tsv
EXPECTED_TSV_CONTENT = (
    "web-01\t10.10.1.11\t8080\tAlice\n"
    "api-01\t10.10.1.21\t9000\tBob\n"
    "db-01\t10.10.1.31\t5432\tCharlie\n"
    "cache-01\t10.10.1.41\t6379\tDavid\n"
    "mq-01\t10.10.1.51\t5672\tEve\n"
)

EXPECTED_LINES = [
    ["web-01", "10.10.1.11", "8080", "Alice"],
    ["api-01", "10.10.1.21", "9000", "Bob"],
    ["db-01", "10.10.1.31", "5432", "Charlie"],
    ["cache-01", "10.10.1.41", "6379", "David"],
    ["mq-01", "10.10.1.51", "5672", "Eve"],
]


def test_environment_directory_exists():
    """The staging directory must exist and be a directory."""
    assert ENV_DIR.exists(), f"Required directory {ENV_DIR} is missing."
    assert ENV_DIR.is_dir(), f"{ENV_DIR} exists but is not a directory."


def test_source_tsv_exists():
    """The source TSV file must exist."""
    assert SRC_FILE.exists(), f"Required file {SRC_FILE} is missing."
    assert SRC_FILE.is_file(), f"{SRC_FILE} exists but is not a regular file."


def test_source_tsv_exact_content():
    """The source TSV file must match the exact expected byte-for-byte content."""
    content = SRC_FILE.read_text(encoding="utf-8")
    assert (
        content == EXPECTED_TSV_CONTENT
    ), (
        f"{SRC_FILE} does not match the expected contents.\n\n"
        "Expected (visible ⟶ TAB, ¶ ⟶ newline):\n"
        + _visualize(EXPECTED_TSV_CONTENT)
        + "\nFound:\n"
        + _visualize(content)
    )


def test_source_tsv_structure():
    """Each line must have exactly four tab-delimited columns with no extra whitespace."""
    lines = SRC_FILE.read_text(encoding="utf-8").splitlines()
    assert lines, f"{SRC_FILE} is empty."
    assert len(lines) == len(
        EXPECTED_LINES
    ), f"{SRC_FILE} should have {len(EXPECTED_LINES)} lines, found {len(lines)}."

    for idx, (expected, line) in enumerate(zip(EXPECTED_LINES, lines), start=1):
        parts = line.split("\t")
        assert (
            parts == expected
        ), f"Line {idx} mismatch.\nExpected: {expected}\nFound:    {parts}"


@pytest.mark.parametrize("path", OUTPUT_FILES, ids=lambda p: str(p))
def test_output_files_absent(path: Path):
    """None of the target output files should exist yet."""
    assert not path.exists(), (
        f"Output file {path} should NOT exist before the student runs any commands.\n"
        "Remove the file and re-run the tests."
    )


# --------------------------------------------------------------------------- #
# Helper function (internal use only)
# --------------------------------------------------------------------------- #
def _visualize(text: str) -> str:
    """
    Return a human-readable representation where TAB = '⟶' and newline = '¶'.
    Useful in assertion error messages.
    """
    return text.replace("\t", "⟶").replace("\n", "¶\n")