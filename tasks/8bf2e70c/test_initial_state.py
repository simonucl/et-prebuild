# test_initial_state.py
#
# This pytest suite validates the *initial* state of the operating-system
# environment **before** the student begins their work.  It confirms that
# the only guaranteed artefact present is the source INI file located at
# /home/user/scan_data/vulnerable-services.ini and that its contents are
# exactly as described in the task specification.  The suite deliberately
# avoids checking for the presence (or absence) of any output artefacts
# such as /home/user/vuln_scan, vuln_report.log, or summary.ini, in
# compliance with the grading rules.

import configparser
from pathlib import Path

import pytest

# Absolute path to the inventory that must already exist
INI_PATH = Path("/home/user/scan_data/vulnerable-services.ini")

# The ground-truth content of the INI file, including its final newline
EXPECTED_INI_CONTENT = (
    "[192.168.1.10-ssh]\n"
    "port = 22\n"
    "service = ssh\n"
    "version = 7.8p1\n"
    "\n"
    "[192.168.1.11-ssh]\n"
    "port = 22\n"
    "service = ssh\n"
    "version = 8.4p1\n"
    "\n"
    "[192.168.1.20-apache]\n"
    "port = 80\n"
    "service = apache\n"
    "version = 2.4.48\n"
    "\n"
    "[192.168.1.21-apache]\n"
    "port = 80\n"
    "service = apache\n"
    "version = 2.4.53\n"
    "\n"
    "[192.168.1.30-mysql]\n"
    "port = 3306\n"
    "service = mysql\n"
    "version = 5.7.37\n"
    "\n"
    "[192.168.1.31-mysql]\n"
    "port = 3306\n"
    "service = mysql\n"
    "version = 8.0.32\n"
)

@pytest.mark.order(1)
def test_ini_file_exists():
    """
    The source inventory file **must** be present before any work begins.
    """
    assert INI_PATH.exists(), (
        f"Required source file not found at {INI_PATH}. "
        "The task cannot proceed without this inventory."
    )
    assert INI_PATH.is_file(), (
        f"{INI_PATH} exists but is not a regular file."
    )

@pytest.mark.order(2)
def test_ini_file_contents_exact_match():
    """
    The inventory file must match the expected byte-for-byte contents.
    A mismatch indicates the starting state is not what the grader expects.
    """
    actual = INI_PATH.read_text(encoding="utf-8")
    assert actual == EXPECTED_INI_CONTENT, (
        "Contents of the inventory file do not match the expected ground-truth.\n"
        "If you modified this file, restore it before running the task."
    )

@pytest.mark.order(3)
def test_ini_is_parseable_and_complete():
    """
    Sanity-check that the INI can be parsed by configparser and that all
    expected sections/keys exist exactly once.
    """
    parser = configparser.ConfigParser()
    parser.read(INI_PATH, encoding="utf-8")

    expected_sections = [
        "192.168.1.10-ssh",
        "192.168.1.11-ssh",
        "192.168.1.20-apache",
        "192.168.1.21-apache",
        "192.168.1.30-mysql",
        "192.168.1.31-mysql",
    ]
    assert parser.sections() == expected_sections, (
        "INI sections differ from the expected ordering or names.\n"
        f"Expected: {expected_sections}\n"
        f"Found:    {parser.sections()}"
    )

    # Validate keys inside each section
    for section in expected_sections:
        for key in ("port", "service", "version"):
            assert key in parser[section], (
                f"Missing key '{key}' in section [{section}] of the inventory file."
            )