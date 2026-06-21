# test_initial_state.py
#
# This test-suite validates the *starting* filesystem state
# for the “Bulk-compress obsolete ticket logs” exercise.
#
# It asserts that:
#   • /home/user/support-logs/ exists and is a directory.
#   • Exactly four regular files are present:
#         ticket_123.log, ticket_124.log, ticket_125.log, README.txt
#   • No *.log.gz archives or compression_summary.txt exist yet.
#   • The contents of the existing files match the specification.
#
# Any failure pin-points what is missing or unexpectedly present so that
# the learner starts from the correct baseline before executing their
# compression pipeline.
#
# Only Python’s stdlib and pytest are used, in keeping with the rules.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
SUPPORT_DIR = HOME / "support-logs"

EXPECTED_FILES = {
    "ticket_123.log",
    "ticket_124.log",
    "ticket_125.log",
    "README.txt",
}

LOG_CONTENTS = {
    "ticket_123.log": "System rebooted OK\n",          # explicit trailing newline
    "ticket_124.log": "Disk cleanup completed",        # newline not guaranteed
    "ticket_125.log": "VPN credentials reset",         # newline not guaranteed
}

README_EXPECTED = (
    "These are daily support logs. Compress old ones regularly."
)


def _read_text(path: Path) -> str:
    """
    Helper to read a text file using UTF-8.  A helpful assertion message
    is raised if the file cannot be read.
    """
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover – any error should fail the test
        pytest.fail(f"Unable to read {path}: {exc}")


def test_support_logs_directory_exists():
    assert SUPPORT_DIR.exists(), f"Directory {SUPPORT_DIR} is missing."
    assert SUPPORT_DIR.is_dir(), f"{SUPPORT_DIR} exists but is not a directory."


def test_expected_files_present_and_no_extras():
    found_files = {p.name for p in SUPPORT_DIR.iterdir() if p.is_file()}
    missing = EXPECTED_FILES - found_files
    extras = found_files - EXPECTED_FILES

    assert not missing, (
        "The following required files are missing from "
        f"{SUPPORT_DIR}: {', '.join(sorted(missing))}"
    )
    assert not extras, (
        "Unexpected extra files found in "
        f"{SUPPORT_DIR}: {', '.join(sorted(extras))}"
    )


def test_no_compressed_or_summary_files_yet():
    gz_files = list(SUPPORT_DIR.glob("*.log.gz"))
    summary_file = SUPPORT_DIR / "compression_summary.txt"

    assert not gz_files, (
        "Compressed *.log.gz files already exist. The initial state must "
        "contain only uncompressed *.log files."
    )

    assert not summary_file.exists(), (
        f"{summary_file} already exists, but it should only be created after "
        "running the compression pipeline."
    )


@pytest.mark.parametrize("filename,expected_content", LOG_CONTENTS.items())
def test_log_file_contents(filename, expected_content):
    path = SUPPORT_DIR / filename
    content = _read_text(path)

    # ticket_123.log must match exactly (including trailing newline)
    if filename == "ticket_123.log":
        assert (
            content == expected_content
        ), f"Content of {filename} does not match the expected exact string."
    else:
        # For the other two logs, allow for an optional trailing newline
        assert content.rstrip("\n") == expected_content, (
            f"Content of {filename} does not match the expected text "
            f"(ignoring a possible trailing newline)."
        )


def test_readme_contents():
    readme_path = SUPPORT_DIR / "README.txt"
    content = _read_text(readme_path).rstrip("\n")
    assert (
        content == README_EXPECTED
    ), "README.txt content does not match the expected text."