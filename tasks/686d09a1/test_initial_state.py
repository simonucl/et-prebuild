# test_initial_state.py
#
# Pytest suite to validate the *initial* state of the filesystem
# before the student carries out any actions described in the task.
#
# The assertions purposefully fail with clear, instructive messages
# if any aspect of the pre-condition is not met.
#
# Rule summary (initial state expected):
#   • /home/user/original_configs/           – directory, exists
#   • /home/user/original_configs/config1.conf  – file, 2 specific lines
#   • /home/user/original_configs/config2.conf  – file, 2 specific lines
#   • /home/user/original_configs/archived/  – must NOT exist yet
#   • /home/user/linked_configs/             – directory, exists & EMPTY
#   • /home/user/config_change.log           – must NOT exist yet

import os
import stat
from pathlib import Path

HOME = Path("/home/user")
ORIG_DIR = HOME / "original_configs"
LINK_DIR = HOME / "linked_configs"
ARCHIVED_DIR = ORIG_DIR / "archived"
LOG_FILE = HOME / "config_change.log"

CONFIG1 = ORIG_DIR / "config1.conf"
CONFIG2 = ORIG_DIR / "config2.conf"

EXPECTED_CONTENTS = {
    CONFIG1: ["version=1.0\n", "name=PrimaryConfig\n"],
    CONFIG2: ["version=2.1\n", "name=SecondaryConfig\n"],
}


def _is_regular_file(path: Path) -> bool:
    """True if path exists and is a regular *non-symlink* file."""
    return path.exists() and path.is_file() and not path.is_symlink()


def test_required_directories_exist_and_archived_absent():
    # original_configs must exist and be a directory
    assert ORIG_DIR.is_dir(), f"Missing directory: {ORIG_DIR}"
    # linked_configs must exist and be a directory
    assert LINK_DIR.is_dir(), f"Missing directory: {LINK_DIR}"
    # archived directory must NOT exist yet
    assert not ARCHIVED_DIR.exists(), (
        f"{ARCHIVED_DIR} should NOT exist before the student runs the task"
    )


def test_linked_configs_is_initially_empty():
    items = list(LINK_DIR.iterdir())
    assert (
        len(items) == 0
    ), f"{LINK_DIR} is expected to be empty, found: {[p.name for p in items]}"


def test_expected_config_files_and_contents():
    for cfg_path, expected_lines in EXPECTED_CONTENTS.items():
        assert _is_regular_file(
            cfg_path
        ), f"Expected a regular file (not symlink) at {cfg_path}"
        with cfg_path.open("r", encoding="utf-8") as fp:
            lines = fp.readlines()

        assert (
            lines == expected_lines
        ), f"File {cfg_path} has unexpected content.\nExpected: {expected_lines!r}\nFound   : {lines!r}"


def test_audit_log_does_not_exist_initially():
    assert not LOG_FILE.exists(), f"{LOG_FILE} must NOT exist in the initial state"