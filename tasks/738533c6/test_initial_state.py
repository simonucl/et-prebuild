# test_initial_state.py
#
# Pytest suite that verifies the operating-system / filesystem state
# *before* the learner runs any commands.  It checks only the pre-populated
# source tree under /home/user/mock_remote/var/www/html and explicitly
# avoids asserting anything about the yet-to-be-created output locations
# (/home/user/pentest/mirror/web01 or /home/user/sync_logs).
#
# Requirements verified:
#     • The source directory exists.
#     • Exactly three regular files are present.
#     • Each expected file exists with the correct size and first-line snippet.
#
# If any assertion fails, the error message pinpoints the missing or
# mismatched element so the learner knows what the environment should
# contain before proceeding.

import os
import pathlib
import pytest

# Constants for the expected source tree
SRC_ROOT = pathlib.Path("/home/user/mock_remote/var/www/html")

EXPECTED_FILES = {
    SRC_ROOT / "index.php": {
        "size": 1254,
        "head": "<?php",
    },
    SRC_ROOT / "admin" / "login.php": {
        "size": 2048,
        "head": "<?php",
    },
    SRC_ROOT / "css" / "style.css": {
        "size": 512,
        "head": "body {",
    },
}

@pytest.fixture(scope="module")
def _src_tree_exists():
    """Ensure the source root exists and is a directory."""
    assert SRC_ROOT.is_dir(), (
        f"Expected source directory '{SRC_ROOT}' to exist and be a directory."
    )
    return SRC_ROOT


def test_expected_files_present_and_correct(_src_tree_exists):
    """Verify each expected file exists, has the correct byte size and header."""
    for path, props in EXPECTED_FILES.items():
        assert path.is_file(), f"Missing expected file: {path}"
        actual_size = path.stat().st_size
        assert actual_size == props["size"], (
            f"File {path} expected size {props['size']} bytes, found {actual_size} bytes."
        )

        # Read first line (decode errors ignored to survive binary edge-cases)
        with path.open("r", errors="ignore") as fh:
            first_line = fh.readline().strip()
        assert first_line.startswith(props["head"]), (
            f"File {path} first line expected to start with '{props['head']}', "
            f"found '{first_line}'."
        )


def test_no_extra_regular_files(_src_tree_exists):
    """Ensure there are no extra regular files beyond the expected three."""
    regular_files = [
        pathlib.Path(root) / fname
        for root, _, files in os.walk(SRC_ROOT)
        for fname in files
    ]
    expected_set = set(EXPECTED_FILES.keys())
    extra_files = set(regular_files) - expected_set
    missing_files = expected_set - set(regular_files)

    assert not missing_files, (
        "The following expected files are missing from the source tree:\n"
        + "\n".join(sorted(map(str, missing_files)))
    )
    assert not extra_files, (
        "Found unexpected files in the source tree (should contain only the three "
        "specified files):\n" + "\n".join(sorted(map(str, extra_files)))
    )

    # Sanity: total file count exactly three
    assert len(regular_files) == 3, (
        f"Source directory should contain exactly 3 regular files, found "
        f"{len(regular_files)}."
    )