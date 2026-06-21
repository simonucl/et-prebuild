# test_initial_state.py
#
# This test-suite validates the *initial* sandbox state *before* the student
# performs any action.  It checks that the template is present while the two
# artefacts the student must create are **not** yet on disk.  If any of these
# pre-conditions are violated the failure message will make the problem clear.

import os
import pytest
from pathlib import Path

# Constants for paths used throughout the tests
INCIDENTS_DIR = Path("/home/user/incidents")
TEMPLATE_MD   = INCIDENTS_DIR / "INCIDENT_TEMPLATE.md"
TARGET_MD     = INCIDENTS_DIR / "INC0001_2024-02-15.md"
LINT_LOG      = INCIDENTS_DIR / "lint_report.log"


def _assert_path_exists(path: Path, is_dir: bool = False):
    """
    Helper: assert that *path* exists and is the requested type (file / dir).
    """
    if not path.exists():
        pytest.fail(f"Required {'directory' if is_dir else 'file'} "
                    f"missing: {path}")
    if is_dir and not path.is_dir():
        pytest.fail(f"Expected a directory at {path}, but found a file.")
    if not is_dir and not path.is_file():
        pytest.fail(f"Expected a file at {path}, but found a directory.")


def _assert_path_absent(path: Path):
    """
    Helper: assert that *path* does NOT yet exist.
    """
    if path.exists():
        pytest.fail(f"{path} should NOT exist before the student starts.")


def test_incidents_directory_exists():
    """
    /home/user/incidents/ must already exist so the student can work within it.
    """
    _assert_path_exists(INCIDENTS_DIR, is_dir=True)


def test_template_file_exists():
    """
    The incident template must be present for the student to fill in.
    """
    _assert_path_exists(TEMPLATE_MD, is_dir=False)

    # Sanity-check that the template is not empty (helps catch accidental removal)
    if TEMPLATE_MD.stat().st_size == 0:
        pytest.fail(f"{TEMPLATE_MD} exists but is empty; it should contain "
                    f"placeholder text for the incident report.")


def test_target_markdown_absent():
    """
    The finished incident report should NOT exist yet.
    """
    _assert_path_absent(TARGET_MD)


def test_lint_report_absent():
    """
    The linter report should NOT exist yet.
    """
    _assert_path_absent(LINT_LOG)