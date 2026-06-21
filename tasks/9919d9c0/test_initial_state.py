# test_initial_state.py
#
# This test-suite verifies that the operating-system / file-system is in the
# expected *pre-migration* state, i.e. nothing from the migration task has been
# created yet.  If any of these tests fail it means that the environment is
# not clean and the student must start from a pristine system before beginning
# the exercise.
#
# The tests purposefully check that:
#   • Required directories do NOT exist yet.
#   • Maintenance scripts are NOT present / executable.
#   • The user’s crontab does NOT already contain the managed block.
#   • No verification manifest exists.
#
# Only Python’s stdlib and pytest are used.

import os
import stat
import subprocess
import textwrap

import pytest

HOME = "/home/user"
BIN_DIR = os.path.join(HOME, "bin")
LOG_DIR = os.path.join(HOME, "logs")
REPORT_DIR = os.path.join(HOME, "reports")
MIGRATION_DIR = os.path.join(HOME, "migration")

REQUIRED_DIRS = [BIN_DIR, LOG_DIR, REPORT_DIR, MIGRATION_DIR]

SCRIPTS = {
    "db_sync.sh": os.path.join(BIN_DIR, "db_sync.sh"),
    "cache_cleanup.sh": os.path.join(BIN_DIR, "cache_cleanup.sh"),
    "weekly_report.sh": os.path.join(BIN_DIR, "weekly_report.sh"),
}

CRONTAB_BLOCK = textwrap.dedent(
    """\
    # ===== Managed by CloudMigrationTool v1 =====
    # Do NOT edit manually
    17 */2 * * * /home/user/bin/db_sync.sh
    30 2 * * * /home/user/bin/cache_cleanup.sh
    45 5 * * 0 /home/user/bin/weekly_report.sh
    # ===== End managed section ====="""
)

MANIFEST_PATH = os.path.join(MIGRATION_DIR, "cron_setup_manifest.txt")


@pytest.mark.parametrize("path", REQUIRED_DIRS)
def test_required_directories_absent(path):
    """
    None of the migration directories should exist before the student starts.
    """
    assert not os.path.exists(
        path
    ), f"Directory '{path}' should NOT exist yet. Start from a clean slate."


@pytest.mark.parametrize("script_name, script_path", SCRIPTS.items())
def test_scripts_absent(script_name, script_path):
    """
    The maintenance scripts must not be present before the exercise starts.
    """
    assert not os.path.exists(
        script_path
    ), f"Script '{script_path}' unexpectedly exists. Ensure you begin with a pristine environment."


@pytest.mark.parametrize("script_name, script_path", SCRIPTS.items())
def test_no_executable_bits_on_missing_scripts(script_name, script_path):
    """
    If, unexpectedly, a script *does* exist, ensure it is NOT marked executable.
    """
    if os.path.exists(script_path):
        mode = os.stat(script_path).st_mode
        is_executable = bool(mode & stat.S_IXUSR)
        assert (
            not is_executable
        ), f"Script '{script_path}' is executable but should not exist yet."


def test_crontab_does_not_contain_managed_block():
    """
    The user's crontab must either be empty or not already contain the managed
    block that the migration will later install.
    """
    try:
        result = subprocess.run(
            ["crontab", "-l"],
            check=False,
            capture_output=True,
            text=True,
            env={"LANG": "C", "LC_ALL": "C"},
        )
    except FileNotFoundError:
        pytest.skip("crontab command not present on this system.")

    # crontab -l exits with 0 if a crontab exists, 1 if none exists
    crontab_text = result.stdout if result.returncode == 0 else ""

    assert (
        CRONTAB_BLOCK not in crontab_text
    ), "The managed cron block is already present in the crontab. The environment must be clean."


def test_manifest_absent():
    """
    The verification manifest must not exist before the migration scripts
    are run.
    """
    assert not os.path.exists(
        MANIFEST_PATH
    ), f"Manifest file '{MANIFEST_PATH}' already exists. Remove it before starting the exercise."