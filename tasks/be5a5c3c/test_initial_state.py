# test_initial_state.py
#
# This pytest suite validates the *initial* filesystem state
# before the student performs any actions.  It checks that:
#   1. The original “docs” directory and its three Markdown files exist
#      and contain the expected contents.
#   2. The “/home/user/backups” and “/home/user/restore” directories
#      already exist and are empty.
# It deliberately does NOT inspect any of the files or directories
# that the student is expected to create (archive, restored copy, log).

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
DOCS_DIR = HOME / "docs"
BACKUPS_DIR = HOME / "backups"
RESTORE_DIR = HOME / "restore"


@pytest.mark.parametrize(
    "path, expected_content",
    [
        (
            DOCS_DIR / "README.md",
            "# Documentation\n\nThis is the README.\n",
        ),
        (
            DOCS_DIR / "architecture.md",
            "# Architecture\n\nSystem overview.\n",
        ),
        (
            DOCS_DIR / "user_guide.md",
            "# User Guide\n\nHow to use the system.\n",
        ),
    ],
)
def test_docs_files_exist_with_correct_content(path: Path, expected_content: str):
    """
    Each required markdown file should exist at the full, explicit path
    and contain the exact expected contents.
    """
    assert path.is_file(), (
        f"Expected file not found: {path}. "
        "Ensure the initial repository contains this file."
    )

    actual = path.read_text(encoding="utf-8")
    assert (
        actual == expected_content
    ), f"Contents of {path} do not match the expected initial text."


def test_docs_directory_structure():
    """
    The /home/user/docs directory itself must exist and be a directory.
    """
    assert DOCS_DIR.is_dir(), (
        f"Directory {DOCS_DIR} is missing. "
        "The initial state must provide the docs directory."
    )


def _dir_is_empty(directory: Path) -> bool:
    """Return True if the directory exists and is empty."""
    return directory.is_dir() and not any(directory.iterdir())


@pytest.mark.parametrize("directory", [BACKUPS_DIR, RESTORE_DIR])
def test_empty_directories_exist(directory: Path):
    """
    /home/user/backups and /home/user/restore must already exist and be empty.
    """
    assert directory.is_dir(), (
        f"Expected directory {directory} to exist in the initial filesystem."
    )

    # They should be empty at the very start.
    assert _dir_is_empty(
        directory
    ), f"Directory {directory} should be empty in the initial state."


# Sanity-check that no output artefacts accidentally exist yet.
@pytest.mark.parametrize(
    "unexpected_path",
    [
        BACKUPS_DIR / "docs_backup.tar.gz",
        RESTORE_DIR / "docs_restored",
        HOME / "backup_log.txt",
    ],
)
def test_no_output_files_yet(unexpected_path: Path):
    """
    Ensure none of the artefacts the student is supposed to create
    are present in the initial state.
    """
    assert not unexpected_path.exists(), (
        f"{unexpected_path} should NOT exist before the task is started."
    )