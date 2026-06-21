# test_initial_state.py
#
# This pytest suite verifies that the operating-system / filesystem
# is in the correct *initial* state before the student performs any
# actions for the “version-locked Markdown backup” task.
#
# EXPECTED INITIAL STATE (truth value)
# ------------------------------------
# 1. Exactly three Markdown files exist—*and nothing else*—inside
#    /home/user/documentation:
#       • overview.md        (specific header line)
#       • getting_started.md (specific header line)
#       • api_reference.md   (specific header line)
# 2. No /home/user/backups directory (or any of its expected files)
#    exists yet.
#
# If any assertion in this file fails, the exercise runner itself is
# mis-configured; the student should not be penalised.

import os
from pathlib import Path

DOC_DIR = Path("/home/user/documentation")
BACKUP_DIR = Path("/home/user/backups")

EXPECTED_MD_FILES = {
    "overview.md": "# Project Overview",
    "getting_started.md": "# Getting Started",
    "api_reference.md": "# API Reference",
}


def test_documentation_directory_exists_and_is_directory():
    assert DOC_DIR.exists(), f"Expected directory {DOC_DIR} is missing."
    assert DOC_DIR.is_dir(), f"{DOC_DIR} exists but is not a directory."


def test_expected_markdown_files_exist_with_correct_headers():
    """
    Ensure each expected *.md file exists, is a regular file,
    and contains the mandated first-line header.
    """
    for filename, header_line in EXPECTED_MD_FILES.items():
        path = DOC_DIR / filename
        assert path.exists(), f"Missing file: {path}"
        assert path.is_file(), f"{path} exists but is not a regular file."

        # Read first non-empty line to compare header.
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped:
                    first_non_empty = stripped
                    break
            else:
                first_non_empty = ""

        assert (
            first_non_empty == header_line
        ), f"{path} does not start with expected header '{header_line}'."


def test_no_extra_markdown_files_present():
    """
    Confirm that NO additional *.md files are present in /home/user/documentation.
    """
    md_files_on_disk = {p.name for p in DOC_DIR.glob("*.md")}
    assert (
        md_files_on_disk == set(EXPECTED_MD_FILES.keys())
    ), (
        "Unexpected Markdown files detected.\n"
        f"Expected: {sorted(EXPECTED_MD_FILES.keys())}\n"
        f"Found   : {sorted(md_files_on_disk)}"
    )


def test_backups_directory_does_not_yet_exist():
    assert not BACKUP_DIR.exists(), (
        f"{BACKUP_DIR} already exists, but the student has not yet "
        "performed the backup operation. The initial state should NOT "
        "contain this directory."
    )


def test_backup_artifacts_do_not_exist():
    """
    Explicitly verify that neither the tarball nor the manifest file exists.
    """
    tar_path = BACKUP_DIR / "doc_backup_20230815.tar.gz"
    manifest_path = BACKUP_DIR / "backup_manifest.log"

    assert not tar_path.exists(), (
        f"Archive {tar_path} already exists before the task starts."
    )
    assert not manifest_path.exists(), (
        f"Manifest {manifest_path} already exists before the task starts."
    )