# test_initial_state.py
#
# This test-suite validates that the filesystem is in the **initial** state,
# i.e. *before* the student begins to work on the assignment.  It checks for
# the presence and exact content of the two source CSV files and confirms that
# the output artefacts and log directory are not yet present.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user").expanduser()
PROJECT_DIR = HOME / "project"
TRANSLATIONS_DIR = PROJECT_DIR / "translations"
LOGS_DIR = PROJECT_DIR / "logs"

EN_US_CSV = TRANSLATIONS_DIR / "en_US.csv"
UPDATES_FR_CSV = TRANSLATIONS_DIR / "updates_fr.csv"
FR_FR_CSV = TRANSLATIONS_DIR / "fr_FR.csv"
MERGE_LOG = LOGS_DIR / "merge.log"


@pytest.fixture(scope="session")
def expected_en_us_content():
    return (
        "id,source_en\n"
        "BTN_OK,OK\n"
        "BTN_CANCEL,Cancel\n"
        "MSG_HELLO,Hello\n"
        "MSG_BYE,Goodbye\n"
        "LBL_NAME,Name\n"
        "LBL_EMAIL,Email\n"
        "ERR_NOTFOUND,Not Found\n"
        "ERR_ACCESS,Access Denied\n"
    )


@pytest.fixture(scope="session")
def expected_updates_fr_content():
    return (
        "id,translation_fr\n"
        "BTN_OK,OK\n"
        "BTN_CANCEL,Annuler\n"
        "MSG_HELLO,Bonjour\n"
        "MSG_BYE,Au revoir\n"
        "LBL_NAME,Nom\n"
        "LBL_EMAIL,E-mail\n"
        "ERR_NOTFOUND,Introuvable\n"
        "ERR_ACCESS,Accès refusé\n"
    )


def test_translations_directory_exists():
    assert TRANSLATIONS_DIR.is_dir(), (
        f"Required directory missing: {TRANSLATIONS_DIR}"
    )


def test_en_us_csv_exists_and_content(expected_en_us_content):
    assert EN_US_CSV.is_file(), f"Missing file: {EN_US_CSV}"
    content = EN_US_CSV.read_text(encoding="utf-8")
    assert content == expected_en_us_content, (
        f"Content of {EN_US_CSV} is not as expected."
    )
    assert content.endswith("\n"), f"{EN_US_CSV} must end with a trailing newline."


def test_updates_fr_csv_exists_and_content(expected_updates_fr_content):
    assert UPDATES_FR_CSV.is_file(), f"Missing file: {UPDATES_FR_CSV}"
    content = UPDATES_FR_CSV.read_text(encoding="utf-8")
    assert content == expected_updates_fr_content, (
        f"Content of {UPDATES_FR_CSV} is not as expected."
    )
    assert content.endswith("\n"), f"{UPDATES_FR_CSV} must end with a trailing newline."


def test_output_files_absent():
    assert not FR_FR_CSV.exists(), (
        f"Output file should not exist yet: {FR_FR_CSV}"
    )
    assert not MERGE_LOG.exists(), (
        f"Log file should not exist yet: {MERGE_LOG}"
    )


def test_logs_directory_absent():
    # The specification says /project/logs/ will be absent initially.
    assert not LOGS_DIR.exists(), (
        f"Directory {LOGS_DIR} should not exist before the student starts."
    )