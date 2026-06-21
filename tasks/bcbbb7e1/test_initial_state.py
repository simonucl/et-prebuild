# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state that must be
# present BEFORE the student runs their solution script.  If any of these
# tests fail, the environment is not in the expected clean state and the
# task cannot be graded reliably.

import os
from pathlib import Path

SCRIPTS_DIR = Path("/home/user/scripts")
ARCHIVES_DIR = Path("/home/user/archives")
LOGS_DIR = Path("/home/user/logs")
RESTORED_DIR = Path("/home/user/restored_scripts")

HELLO_PATH = SCRIPTS_DIR / "hello.sh"
README_PATH = SCRIPTS_DIR / "README.md"

# Expected file contents (UTF-8, trailing newline optional)
EXPECTED_HELLO_CONTENT = (
    "#!/usr/bin/env bash\n"
    "echo \"Hello, World!\"\n"
)

EXPECTED_README_CONTENT = (
    "# Utility Scripts\n"
    "This directory contains small helper scripts used in various automation tasks.\n"
)


def _read_file_strip(path: Path) -> str:
    """
    Helper: read a text file as UTF-8 and strip trailing
    whitespace so we can tolerate the presence/absence of a
    final newline character.
    """
    with path.open("r", encoding="utf-8") as fh:
        return fh.read().rstrip()


def test_scripts_directory_exists_and_has_exact_two_files():
    assert SCRIPTS_DIR.is_dir(), (
        f"Required directory {SCRIPTS_DIR} is missing or not a directory."
    )

    entries = sorted(p.name for p in SCRIPTS_DIR.iterdir() if p.is_file())
    expected_entries = ["README.md", "hello.sh"]
    assert entries == expected_entries, (
        f"{SCRIPTS_DIR} should contain exactly the files "
        f"{expected_entries}, but found: {entries or 'nothing'}."
    )


def test_hello_sh_exists_and_contents_correct():
    assert HELLO_PATH.is_file(), (
        f"Expected file {HELLO_PATH} does not exist."
    )
    actual = _read_file_strip(HELLO_PATH)
    expected = EXPECTED_HELLO_CONTENT.rstrip()
    assert actual == expected, (
        f"Contents of {HELLO_PATH} do not match expected template.\n"
        f"Expected:\n{expected!r}\n\nFound:\n{actual!r}"
    )


def test_readme_md_exists_and_contents_correct():
    assert README_PATH.is_file(), (
        f"Expected file {README_PATH} does not exist."
    )
    actual = _read_file_strip(README_PATH)
    expected = EXPECTED_README_CONTENT.rstrip()
    assert actual == expected, (
        f"Contents of {README_PATH} do not match expected template.\n"
        f"Expected:\n{expected!r}\n\nFound:\n{actual!r}"
    )


def test_archives_directory_exists_and_is_empty():
    assert ARCHIVES_DIR.is_dir(), (
        f"Required directory {ARCHIVES_DIR} is missing or not a directory."
    )

    files = [p for p in ARCHIVES_DIR.iterdir() if p.is_file()]
    assert not files, (
        f"{ARCHIVES_DIR} should be empty before the task starts; "
        f"found unexpected files: {[p.name for p in files]}"
    )


def test_logs_directory_exists_and_is_empty():
    assert LOGS_DIR.is_dir(), (
        f"Required directory {LOGS_DIR} is missing or not a directory."
    )

    files = [p for p in LOGS_DIR.iterdir() if p.is_file()]
    assert not files, (
        f"{LOGS_DIR} should be empty before the task starts; "
        f"found unexpected files: {[p.name for p in files]}"
    )


def test_restored_scripts_directory_does_not_exist_yet():
    assert not RESTORED_DIR.exists(), (
        f"Directory {RESTORED_DIR} should NOT exist before the task starts, "
        "but it is already present."
    )