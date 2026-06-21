# test_initial_state.py
#
# Pytest suite that verifies the *initial* operating-system / filesystem
# layout before the student performs any actions for the “permission-aware
# file-synchronisation” assignment.
#
# Only stdlib + pytest are used, and every failure message explains exactly
# what is missing or wrong so that students can fix the environment before
# working on their solution.

import os
import stat
from pathlib import Path

PROJECT_ROOT = Path("/home/user/project")
PUBLIC_DIR   = PROJECT_ROOT / "public"
DEST_ROOT    = Path("/home/user/simulated_remote")
REPORT_FILE  = Path("/home/user/sync_report.log")


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def octal_permissions(p: Path) -> str:
    """Return a file’s permissions as a zero-padded 3-digit octal string."""
    return format(p.stat().st_mode & 0o777, "03o")


def is_world_readable(p: Path) -> bool:
    """True iff the file’s ‘other’ read bit is set."""
    return bool(p.stat().st_mode & stat.S_IROTH)


# --------------------------------------------------------------------------- #
# 1. Basic directory structure
# --------------------------------------------------------------------------- #
def test_directories_exist_and_are_empty_where_expected():
    # Source tree must exist.
    assert PROJECT_ROOT.is_dir(), f"Missing source directory: {PROJECT_ROOT}"

    # Public sub-directory must exist.
    assert PUBLIC_DIR.is_dir(), f"Missing sub-directory: {PUBLIC_DIR}"

    # Destination tree must exist and be *empty* before the sync.
    assert DEST_ROOT.is_dir(), f"Missing destination directory: {DEST_ROOT}"
    dest_contents = list(DEST_ROOT.iterdir())
    assert not dest_contents, (
        f"Destination directory {DEST_ROOT} is not empty before sync:\n"
        f"Contents found: {[p.name for p in dest_contents]}"
    )

    # The report file must *not* exist yet.
    assert not REPORT_FILE.exists(), (
        f"Report file {REPORT_FILE} should not exist before the sync."
    )


# --------------------------------------------------------------------------- #
# 2. Individual files, their permissions and contents
# --------------------------------------------------------------------------- #
FILE_FIXTURES = [
    # (absolute_path, expected_contents, expected_octal_permissions)
    (PROJECT_ROOT / "index.html",        "<html>Index</html>\n",     "644"),
    (PROJECT_ROOT / "secret.txt",        "top secret\n",             "600"),
    (PROJECT_ROOT / "readme.md",         "Project read-me\n",        "664"),
    (PROJECT_ROOT / ".env",              "DB_PASS=1234\n",           "600"),
    (PUBLIC_DIR   / "style.css",         "body {margin:0;}\n",       "644"),
    (PUBLIC_DIR   / "script.sh",         "#!/bin/bash\necho hi\n",   "755"),
]


import pytest


@pytest.mark.parametrize("file_path, expected_content, expected_perm", FILE_FIXTURES)
def test_files_exist_with_correct_contents_and_permissions(
    file_path: Path,
    expected_content: str,
    expected_perm: str,
):
    # Existence & type -------------------------------------------------------
    assert file_path.exists(), f"Expected file missing: {file_path}"
    assert file_path.is_file(), f"Path is not a file: {file_path}"

    # Permissions -----------------------------------------------------------
    perm = octal_permissions(file_path)
    assert perm == expected_perm, (
        f"Permissions for {file_path} are {perm}, expected {expected_perm}"
    )

    # Contents --------------------------------------------------------------
    with file_path.open("r", encoding="utf-8") as fh:
        actual_content = fh.read()
    assert actual_content == expected_content, (
        f"Contents of {file_path} do not match expected value.\n"
        f"EXPECTED ({len(expected_content)} bytes): {repr(expected_content)}\n"
        f"FOUND    ({len(actual_content)} bytes): {repr(actual_content)}"
    )


# --------------------------------------------------------------------------- #
# 3. Classification of world-readable vs. private files
# --------------------------------------------------------------------------- #
def test_world_readable_file_set_is_correct():
    expected_world_readable = {
        Path("index.html"),
        Path("public/style.css"),
        Path("public/script.sh"),
        Path("readme.md"),
    }

    # Discover actual world-readable files in the project tree.
    actual_world_readable = set()
    for p in PROJECT_ROOT.rglob("*"):
        # Skip directories.
        if not p.is_file():
            continue
        if is_world_readable(p):
            actual_world_readable.add(p.relative_to(PROJECT_ROOT))

    assert actual_world_readable == expected_world_readable, (
        "Mismatch in world-readable file detection.\n"
        f"EXPECTED: {[str(p) for p in sorted(expected_world_readable)]}\n"
        f"FOUND   : {[str(p) for p in sorted(actual_world_readable)]}"
    )