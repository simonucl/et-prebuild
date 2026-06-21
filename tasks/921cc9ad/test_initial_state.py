# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state before the student performs any action for the “static web-site
# restore” exercise.
#
# It asserts that only the expected pre-existing artefacts are present:
#   • Directory /home/user/backup
#   • File      /home/user/backup/site_backup.tar.gz
#
# It also checks that:
#   • The tarball contains a single entry “index.html” whose contents match
#     the specification.
#   • The restoration target directory (/home/user/restored_site) as well as
#     the log file (/home/user/restoration.log) do *not* yet exist.
#
# No third-party modules are used; only Python’s stdlib and pytest.

import os
import tarfile
import pytest

BACKUP_DIR = "/home/user/backup"
TARBALL = os.path.join(BACKUP_DIR, "site_backup.tar.gz")
RESTORE_DIR = "/home/user/restored_site"
LOG_FILE = "/home/user/restoration.log"

EXPECTED_HTML = (
    "<html>\n"
    "<body>\n"
    "<h1>Backup Restore Successful</h1>\n"
    "</body>\n"
    "</html>\n"
)


def test_backup_directory_exists():
    assert os.path.isdir(
        BACKUP_DIR
    ), f"Required backup directory {BACKUP_DIR} is missing."


def test_backup_tarball_exists():
    assert os.path.isfile(
        TARBALL
    ), f"Required backup tarball {TARBALL} is missing."


def test_tarball_contains_expected_index_html():
    # Ensure the tarball can be opened
    try:
        with tarfile.open(TARBALL, "r:gz") as tf:
            members = tf.getnames()
            assert members, "The tarball is empty."
            assert members == ["index.html"], (
                f"The tarball should contain exactly one entry named "
                f"'index.html', found: {members}"
            )

            # Read the file contents and compare to expectation
            extracted = tf.extractfile("index.html")
            assert extracted is not None, "Failed to read 'index.html' from tarball."
            content = extracted.read().decode("utf-8")
            assert (
                content == EXPECTED_HTML
            ), "Contents of 'index.html' in tarball do not match the expected HTML."
    except tarfile.ReadError as e:
        pytest.fail(f"Unable to open tarball {TARBALL}: {e}")


def test_restore_directory_does_not_yet_exist():
    assert not os.path.exists(
        RESTORE_DIR
    ), (
        f"The directory {RESTORE_DIR} already exists, but it should be created "
        f"only by the restoration script."
    )


def test_restoration_log_does_not_yet_exist():
    assert not os.path.exists(
        LOG_FILE
    ), (
        f"The log file {LOG_FILE} already exists, but it should be created "
        f"only after successful restoration."
    )