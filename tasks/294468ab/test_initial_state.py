# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student performs any action.

import os
import stat
import textwrap
from pathlib import Path

import pytest


HOME = Path("/home/user")
MOCK_SITE_DIR = HOME / "mock_site"
BACKUP_DIR = HOME / "backup"
DATA_HTML = MOCK_SITE_DIR / "data.html"


EXPECTED_HTML_CONTENT = textwrap.dedent("""\
    <html>
    <body>
    <h1>Daily Backup Report</h1>
    <p>ARCHIVE: db_full_2023-08-04.tar.gz</p>
    <p>ARCHIVE: logs_2023-08-04.tar.gz</p>
    <p>STATUS: Completed</p>
    </body>
    </html>
    """).splitlines(keepends=True)


@pytest.mark.describe("Initial directory layout is correct")
def test_directories_exist_and_are_correct():
    # /home/user/mock_site must exist and be a directory
    assert MOCK_SITE_DIR.is_dir(), (
        f"Expected directory {MOCK_SITE_DIR} to exist before you start, "
        "but it is missing."
    )

    # /home/user/backup must exist and be a directory
    assert BACKUP_DIR.is_dir(), (
        f"Expected directory {BACKUP_DIR} to exist before you start, "
        "but it is missing."
    )

    # /home/user/backup must be writable by the current user
    assert os.access(BACKUP_DIR, os.W_OK), (
        f"Directory {BACKUP_DIR} exists but is not writable. "
        "Make sure you have write permissions."
    )


@pytest.mark.describe("data.html is present and has the expected contents")
def test_mock_site_contains_correct_html_file():
    # File must exist
    assert DATA_HTML.is_file(), (
        f"Expected file {DATA_HTML} to exist before you start, but it is missing."
    )

    # data.html must be the only file in /home/user/mock_site
    extra_files = [
        p for p in MOCK_SITE_DIR.iterdir()
        if p.is_file() and p != DATA_HTML
    ]
    assert not extra_files, (
        f"Directory {MOCK_SITE_DIR} should contain only {DATA_HTML.name}, "
        f"but found additional file(s): {[str(p) for p in extra_files]}"
    )

    # Read file and compare exact byte content
    with DATA_HTML.open("rb") as fh:
        actual_bytes = fh.read()

    expected_bytes = "".join(EXPECTED_HTML_CONTENT).encode()
    assert actual_bytes == expected_bytes, (
        f"File {DATA_HTML} does not match the expected contents.\n"
        "If your text editor added or removed whitespace/newlines, "
        "revert the file back to the exact original state."
    )