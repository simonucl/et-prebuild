# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the filesystem
# before the student has created any new automation.  It checks that
# the legacy web-site is present and that no script / log artefacts
# exist yet.  All paths are absolute, rooted at /home/user.

import os
from pathlib import Path

WEBSITE_ROOT = Path("/home/user/my_website")
PUBLIC_DIR = WEBSITE_ROOT / "public"
EXPECTED_HTML_FILES = {"index.html", "about.html", "contact.html"}

SCRIPT_PATH = Path("/home/user/scripts/build_logs.sh")
BUILD_LOGS_DIR = Path("/home/user/build_logs")
SUMMARY_LOG_PATH = BUILD_LOGS_DIR / "summary.log"


def test_website_root_exists():
    assert WEBSITE_ROOT.is_dir(), (
        f"Expected directory {WEBSITE_ROOT} to exist, "
        "but it was not found."
    )


def test_public_dir_exists():
    assert PUBLIC_DIR.is_dir(), (
        f"Expected directory {PUBLIC_DIR} to exist, "
        "but it was not found."
    )


def test_exact_three_html_files_present():
    html_files = {p.name for p in PUBLIC_DIR.glob("*.html")}
    missing = EXPECTED_HTML_FILES - html_files
    unexpected = html_files - EXPECTED_HTML_FILES

    assert not missing, (
        "The following required HTML files are missing from "
        f"{PUBLIC_DIR}: {', '.join(sorted(missing))}"
    )
    assert not unexpected, (
        f"The directory {PUBLIC_DIR} contains unexpected HTML files: "
        f"{', '.join(sorted(unexpected))}"
    )
    assert len(html_files) == 3, (
        f"Expected exactly 3 HTML files in {PUBLIC_DIR}, "
        f"but found {len(html_files)}."
    )


def test_build_script_not_yet_present():
    assert not SCRIPT_PATH.exists(), (
        f"The build script {SCRIPT_PATH} should NOT exist yet. "
        "Create it only when implementing the task."
    )


def test_build_logs_not_yet_present():
    # Neither the directory nor the summary log should exist yet.
    assert not BUILD_LOGS_DIR.exists(), (
        f"The directory {BUILD_LOGS_DIR} should NOT exist yet."
    )
    assert not SUMMARY_LOG_PATH.exists(), (
        f"The log file {SUMMARY_LOG_PATH} should NOT exist yet."
    )