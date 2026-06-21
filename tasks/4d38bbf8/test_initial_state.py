# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem BEFORE the
# student performs any action for the “deterministic backup” exercise.
#
# It checks that:
#   • /home/user/important_data exists with the expected sub-tree.
#   • Key text files contain the expected lines.
#   • Binary placeholder files are present and non-empty.
#   • /home/user/backups does NOT yet exist.
#
# No output/artefact paths (tar.gz, .sha256, log files, …) are inspected here,
# because they must be created by the student **after** this initial state.

import os
from pathlib import Path

ROOT_IMPORTANT = Path("/home/user/important_data")
BACKUPS_DIR = Path("/home/user/backups")


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def assert_file_contains(path: Path, expected_substrings, *, msg_hint=""):
    """
    Assert that `path` exists, is a file, and that each substring in
    `expected_substrings` occurs somewhere in the file’s content.
    """
    assert path.exists(), f"Missing file: {path}{msg_hint}"
    assert path.is_file(), f"Expected a regular file at {path}{msg_hint}"
    text = path.read_text(encoding="utf-8", errors="replace")
    for sub in expected_substrings:
        assert sub in text, (
            f"File {path} is missing expected text:\n"
            f"   `{sub}`\n"
            f"{msg_hint}"
        )


def assert_nonempty_file(path: Path, *, msg_hint=""):
    """
    Assert that `path` exists, is a file, and has a size > 0 bytes.
    """
    assert path.exists(), f"Missing file: {path}{msg_hint}"
    assert path.is_file(), f"{path} exists but is not a regular file{msg_hint}"
    assert path.stat().st_size > 0, f"File {path} is empty{msg_hint}"


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_important_data_directory_exists():
    assert ROOT_IMPORTANT.exists(), (
        f"The directory {ROOT_IMPORTANT} must exist before you start."
    )
    assert ROOT_IMPORTANT.is_dir(), (
        f"{ROOT_IMPORTANT} exists but is not a directory."
    )


def test_expected_tree_structure():
    """
    Verify that the full directory / file structure expected by management is
    present under /home/user/important_data.
    """
    expected_paths = [
        ROOT_IMPORTANT / "config" / "settings.conf",
        ROOT_IMPORTANT / "projectA" / "data.csv",
        ROOT_IMPORTANT / "projectA" / "report.txt",
        ROOT_IMPORTANT / "projectB" / "figures" / "diagram.png",
        ROOT_IMPORTANT / "projectB" / "presentation.pptx",
    ]

    for p in expected_paths:
        assert p.exists(), f"Missing expected path: {p}"
        if p.suffix in {".png", ".pptx"}:
            # We do not check their exact contents, just that the file is not empty
            assert_nonempty_file(p)
        else:
            # They should be regular files
            assert p.is_file(), f"Expected a regular file at {p}"


def test_config_settings_conf_contents():
    """
    settings.conf should contain the three critical lines:
      • # Application settings
      • mode = production
      • timeout = 30
    Exact formatting of surrounding whitespace or extra comment lines is not
    enforced, only the presence of these substrings.
    """
    path = ROOT_IMPORTANT / "config" / "settings.conf"
    expected_lines = [
        "# Application settings",
        "mode = production",
        "timeout = 30",
    ]
    assert_file_contains(path, expected_lines)


def test_projectA_report_contents():
    """
    projectA/report.txt should at least mention 'Project A quarterly report'.
    """
    path = ROOT_IMPORTANT / "projectA" / "report.txt"
    assert_file_contains(
        path,
        ["Project A quarterly report"],
        msg_hint=" (file content check for report.txt)",
    )


def test_projectA_data_csv_contents():
    """
    projectA/data.csv must contain the header and two rows described in the
    ground-truth specification.
    """
    path = ROOT_IMPORTANT / "projectA" / "data.csv"
    expected_lines = [
        "id,value",
        "1,42",
        "2,97",
    ]
    assert_file_contains(path, expected_lines)


def test_backups_directory_does_not_exist_yet():
    assert not BACKUPS_DIR.exists(), (
        f"The directory {BACKUPS_DIR} should NOT exist before you start. "
        "It must be created by your solution when you run the backup script."
    )