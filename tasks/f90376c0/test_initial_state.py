# test_initial_state.py
#
# Pytest suite to validate the starting state *before* the student carries out
# the “policy-as-code” backup task.  These assertions guarantee that the demo
# environment is set up correctly and that no artefacts from a previous run are
# already present.

import os
import datetime
import re
from pathlib import Path

CONFIG_DIR = Path("/home/user/projects/myapp/config")
BACKUP_DIR = Path("/home/user/backups")
TODAY_YMD = datetime.datetime.now().strftime("%Y%m%d")
TODAY_ARCHIVE = BACKUP_DIR / f"myapp_conf_backup_{TODAY_YMD}.tar.gz"
AUDIT_LOG = BACKUP_DIR / "backup_audit.log"


def test_config_directory_exists():
    assert CONFIG_DIR.is_dir(), (
        f"Required config directory {CONFIG_DIR} is missing. "
        "The automated task cannot proceed without it."
    )


def test_required_conf_files_exist_and_are_readable():
    expected_files = {
        "app.conf",
        "db.conf",
        "secrets.conf",
    }

    present_files = {p.name for p in CONFIG_DIR.iterdir() if p.is_file() and p.suffix == ".conf"}

    missing = expected_files - present_files
    extra = present_files - expected_files

    assert not missing, (
        "The following required .conf files are missing from "
        f"{CONFIG_DIR}: {', '.join(sorted(missing))}"
    )

    # It is acceptable for the directory to contain additional, non-.conf files.
    assert not extra, (
        f"Unexpected .conf files found in {CONFIG_DIR}: {', '.join(sorted(extra))}. "
        "The demo directory should contain *only* the three specified .conf files."
    )

    # Confirm readability
    for fname in expected_files:
        fpath = CONFIG_DIR / fname
        try:
            with fpath.open("r") as fh:
                fh.read(1)
        except Exception as exc:  # noqa: BLE001
            raise AssertionError(f"File {fpath} is not readable: {exc}") from exc


def test_no_backup_tarball_for_today_yet():
    assert not TODAY_ARCHIVE.exists(), (
        f"Backup tarball for today already exists at {TODAY_ARCHIVE}. "
        "The exercise must start with no archive for the current date."
    )


def test_audit_log_has_no_entry_for_today_archive():
    """
    The audit log may already exist from prior test runs, but it must NOT contain
    a line referencing today's archive.  This guarantees that the student task
    will append a *new* record.
    """
    if not AUDIT_LOG.exists():
        # Nothing to check if the log is not present yet.
        return

    pattern = re.compile(
        rf"^\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}} \| OK \| 3 files \| {re.escape(str(TODAY_ARCHIVE))}$"
    )

    with AUDIT_LOG.open("r") as fh:
        for line in fh:
            assert not pattern.match(line.rstrip("\n")), (
                "The audit log already contains an entry for today's backup "
                f"({TODAY_ARCHIVE}).  The log must not have today's line before "
                "the student performs the backup."
            )