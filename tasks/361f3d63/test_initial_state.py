# test_initial_state.py
#
# Pytest suite that validates the **initial** filesystem state for the
# “local-to-remote file-synchronisation” exercise _before_ the student
# performs any action.
#
# The checks enforce that:
#   • Source configuration files exist with the exact expected content.
#   • The simulated remote directory contains only the legacy file.
#   • The yet-to-be-generated log file is **absent**.
#
# If any assertion fails, the accompanying message pinpoints what is
# missing or unexpectedly present.
#
# NOTE:  Do **not** modify this file.  Students must bring the system
#        from this verified starting state to the required final state.

from pathlib import Path
import pytest

HOME = Path("/home/user")
SRC_DIR = HOME / "source_configs"
DST_DIR = HOME / "remote_server" / "configs"
LOG_DIR = HOME / "sync_logs"
LOG_FILE = LOG_DIR / "rsync_sync.log"


@pytest.fixture(scope="module")
def expected_sources():
    """Return a mapping of expected source file names to their exact content."""
    return {
        "app.conf": "APP_ENV=production\nMAX_CLIENTS=200\n",
        "db.conf": "DB_HOST=postgres.internal\nDB_PORT=5432\n",
    }


def test_source_directory_exists():
    assert SRC_DIR.is_dir(), f"Required source directory {SRC_DIR} is missing."


def test_source_files_present_and_content(expected_sources):
    for fname, expected_content in expected_sources.items():
        fpath = SRC_DIR / fname
        assert fpath.is_file(), f"Source file {fpath} is missing."
        raw = fpath.read_text(encoding="utf-8")
        assert raw == expected_content, (
            f"Content of {fpath} does not match the expected initial data."
        )


def test_remote_directory_exists():
    assert DST_DIR.is_dir(), f"Remote directory {DST_DIR} is missing."


def test_remote_contains_only_old_conf_initially():
    old_conf = DST_DIR / "old.conf"
    assert old_conf.is_file(), (
        f"Legacy file {old_conf} must be present before sync begins."
    )

    unexpected_files = {"app.conf", "db.conf"}
    found_unexpected = [p.name for p in DST_DIR.iterdir() if p.name in unexpected_files]
    assert not found_unexpected, (
        f"Unexpected files already exist in the remote directory: {found_unexpected}. "
        "They should be created only by the student’s synchronisation task."
    )


def test_log_file_absent_initially():
    assert not LOG_FILE.exists(), (
        f"Log file {LOG_FILE} should not exist before the synchronisation task runs."
    )