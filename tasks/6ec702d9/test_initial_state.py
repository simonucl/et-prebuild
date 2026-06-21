# test_initial_state.py
#
# This pytest suite asserts the initial, pre-task condition of the
# filesystem.  If any of these assertions fail, the student must fix
# the environment **before** attempting the shell work described in
# the assignment.

import pathlib
import textwrap
import pytest


DB_CONFIG_DIR = pathlib.Path("/home/user/db_configs")
REPORTS_DIR = pathlib.Path("/home/user/reports")
CONNECTION_INI = DB_CONFIG_DIR / "connection.ini"
QUERIES_INI = DB_CONFIG_DIR / "queries.ini"
SLOW_REPORT = REPORTS_DIR / "slow_queries_report.log"


@pytest.fixture(scope="module")
def expected_connection_text():
    """
    The pristine content of /home/user/db_configs/connection.ini
    (final newline included).
    """
    return textwrap.dedent(
        """\
        [development]
        host=localhost
        port=5432
        user=dev
        password=devpass
        pool_size=5

        [staging]
        host=staging.db.internal
        port=5432
        user=staging
        password=stagingpass
        pool_size=10

        [production]
        host=prod.db.internal
        port=5432
        user=prod
        password=prodpass
        pool_size=20
        """
    )


@pytest.fixture(scope="module")
def expected_queries_text():
    """
    The pristine content of /home/user/db_configs/queries.ini
    (final newline included).
    """
    return textwrap.dedent(
        """\
        [number_users]
        query=SELECT COUNT(*) FROM users;
        slow=no
        priority=3

        [big_join]
        query=SELECT u.id, o.id FROM users u JOIN orders o ON u.id=o.user_id;
        slow=yes
        priority=2

        [monthly_report]
        query=SELECT * FROM reports WHERE month=CURRENT_DATE;
        slow=yes
        priority=5

        [tmp_cleanup]
        query=DELETE FROM temp WHERE created_at < NOW() - INTERVAL '1 day';
        slow=no
        priority=1

        [yearly_stats]
        query=SELECT * FROM stats_yearly;
        slow=yes
        priority=4
        """
    )


def normalise_newlines(text: str) -> str:
    """
    Convert CRLF and ensure a single trailing '\n', which is how the
    expected_*_text fixtures are written.
    """
    text = text.replace("\r\n", "\n")
    if not text.endswith("\n"):
        text += "\n"
    return text


def test_db_configs_directory_exists():
    assert DB_CONFIG_DIR.is_dir(), (
        f"Required directory {DB_CONFIG_DIR} is missing. "
        "The initial repository of INI files must be present."
    )


def test_connection_ini_content(expected_connection_text):
    assert CONNECTION_INI.is_file(), (
        f"Expected file {CONNECTION_INI} does not exist."
    )
    actual = normalise_newlines(CONNECTION_INI.read_text(encoding="utf-8"))
    expected = expected_connection_text
    assert actual == expected, (
        f"The content of {CONNECTION_INI} is not the expected pristine state.\n"
        "Hint: no edits should have been made yet.  Differences detected."
    )


def test_queries_ini_content(expected_queries_text):
    assert QUERIES_INI.is_file(), (
        f"Expected file {QUERIES_INI} does not exist."
    )
    actual = normalise_newlines(QUERIES_INI.read_text(encoding="utf-8"))
    expected = expected_queries_text
    assert actual == expected, (
        f"The content of {QUERIES_INI} is not the expected pristine state.\n"
        "Ensure the file has not been modified."
    )


def test_reports_directory_absent():
    """
    Before the task is executed, /home/user/reports/ must NOT exist.
    It should be created by the student script later.
    """
    assert not REPORTS_DIR.exists(), (
        f"Directory {REPORTS_DIR} already exists, but it should not be "
        "present before the task is executed."
    )


def test_slow_report_absent():
    """
    Likewise, the final report file must not exist yet.
    """
    assert not SLOW_REPORT.exists(), (
        f"File {SLOW_REPORT} already exists.  The report is supposed to be "
        "generated only after the student completes the task."
    )