# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state **before**
# the student performs any edits.  It verifies that the two configuration
# files are present with their original contents and that the change-log
# file has NOT been created yet.

from pathlib import Path
import textwrap
import pytest

# Absolute paths that must exist
ROOT_DIR = Path("/home/user/configs")
DB_CFG = ROOT_DIR / "db_config.yaml"
OPT_CFG = ROOT_DIR / "query_optimizer.toml"
CHANGE_LOG = ROOT_DIR / "changes_log.txt"


@pytest.fixture(scope="module")
def expected_db_config_text():
    """
    Expected original content of /home/user/configs/db_config.yaml.

    A trailing newline is included because most editors add one on save.
    The comparison in the tests tolerates the absence of that final \n
    just in case.
    """
    return textwrap.dedent(
        """\
        # Database configuration
        connection:
          host: localhost
          port: 5432
          user: admin
          password: admin123
        performance:
          query_caching: false
          cache_size: 128MB
        """
    )


@pytest.fixture(scope="module")
def expected_opt_config_text():
    """
    Expected original content of /home/user/configs/query_optimizer.toml.
    """
    return textwrap.dedent(
        """\
        # Query optimizer settings
        max_parallel_workers = 2
        enable_hashagg = false
        enable_bitmapscan = true
        """
    )


def _normalize(text: str) -> str:
    """
    Helper that returns *exactly* the text plus a single trailing newline.
    Makes it easier to compare whether the on-disk file has or lacks the
    trailing newline.
    """
    return text if text.endswith("\n") else text + "\n"


def test_configs_directory_exists():
    assert ROOT_DIR.is_dir(), (
        f"Required directory {ROOT_DIR} is missing. "
        "Nothing else can be tested until this directory exists."
    )


def test_db_config_initial_state(expected_db_config_text):
    assert DB_CFG.is_file(), f"Missing file: {DB_CFG}"
    on_disk = DB_CFG.read_text(encoding="utf-8")
    expected = expected_db_config_text
    msg = (
        f"{DB_CFG} contents differ from the expected *initial* state.\n"
        "Did you modify the file before running the initial-state tests?"
    )
    assert on_disk in (_normalize(expected), expected.rstrip("\n")), msg


def test_query_optimizer_initial_state(expected_opt_config_text):
    assert OPT_CFG.is_file(), f"Missing file: {OPT_CFG}"
    on_disk = OPT_CFG.read_text(encoding="utf-8")
    expected = expected_opt_config_text
    msg = (
        f"{OPT_CFG} contents differ from the expected *initial* state.\n"
        "Did you modify the file before running the initial-state tests?"
    )
    assert on_disk in (_normalize(expected), expected.rstrip("\n")), msg


def test_change_log_not_present_yet():
    assert not CHANGE_LOG.exists(), (
        f"{CHANGE_LOG} should NOT exist yet. "
        "The change-log must only be created after the configuration "
        "files have been updated."
    )