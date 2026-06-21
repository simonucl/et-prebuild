# test_initial_state.py
#
# This pytest suite verifies the **initial** state of the operating system
# _before_ the student carries out the assignment.  None of the artefacts
# required by the task should exist yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")
MIGRATION_DIR = HOME / "migration"
SCRIPT_PATH = MIGRATION_DIR / "migrate_fw.sh"
LOG_PATH = MIGRATION_DIR / "firewall_migration.log"


def assert_absent(p: Path):
    """
    Helper that fails with a clear message if the supplied path exists.
    """
    assert not p.exists(), f"Path should NOT exist yet: {p}"


def test_migration_directory_absent():
    """
    /home/user/migration should NOT exist prior to the student's work.
    """
    assert_absent(MIGRATION_DIR)


def test_migration_script_absent():
    """
    /home/user/migration/migrate_fw.sh must NOT exist prior to the student's work.
    """
    assert_absent(SCRIPT_PATH)


def test_firewall_log_absent():
    """
    /home/user/migration/firewall_migration.log must NOT exist prior to the student's work.
    """
    assert_absent(LOG_PATH)