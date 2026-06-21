# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem state
# BEFORE the student script is executed.  These tests assert that only the
# pre-staged template tree exists and that none of the artefacts the student
# is supposed to create are present yet.
#
# The suite deliberately fails fast with clear error messages if any part
# of the expected starting environment is missing or has been modified.

import os
from pathlib import Path

import pytest

PROVISION_ROOT = Path("/home/user/provision")
TEMPLATES_ROOT = PROVISION_ROOT / "templates"
OUTPUT_DIR = PROVISION_ROOT / "output"
ARCHIVE_PATH = PROVISION_ROOT / "config_bundle.tar.gz"
BUILD_LOG = PROVISION_ROOT / "build.log"

# --------------------------------------------------------------------------- #
# Expected template files and their exact byte contents (including newlines). #
# --------------------------------------------------------------------------- #

EXPECTED_TEMPLATES = {
    TEMPLATES_ROOT / "app" / "app.conf.template": (
        "APP_ENV=production\n"
        "PORT=8080\n"
    ),
    TEMPLATES_ROOT / "db" / "db.conf.template": (
        "DB_HOST=localhost\n"
        "DB_PORT=5432\n"
    ),
    TEMPLATES_ROOT / "web" / "nginx.conf.template": (
        "server {\n"
        "    listen 80;\n"
        "    server_name example.com;\n"
        "}\n"
    ),
}


# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #

def _read_text(path: Path) -> str:
    """Read text from `path` using UTF-8, raising a helpful error if it fails."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path}: {exc}")


# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #

def test_templates_directory_exists():
    """The /home/user/provision/templates directory must exist and be a dir."""
    assert TEMPLATES_ROOT.exists(), (
        f"Required directory {TEMPLATES_ROOT} does not exist."
    )
    assert TEMPLATES_ROOT.is_dir(), (
        f"{TEMPLATES_ROOT} exists but is not a directory."
    )


def test_template_subdirectory_structure():
    """'app', 'db', and 'web' subdirectories must exist inside templates/."""
    for sub in ("app", "db", "web"):
        path = TEMPLATES_ROOT / sub
        assert path.exists(), f"Expected subdirectory {path} is missing."
        assert path.is_dir(), f"{path} exists but is not a directory."


def test_expected_template_files_present_and_correct():
    """
    Verify that every expected *.template file exists WITH EXACT CONTENT and that
    no extra files are present inside the templates tree.
    """
    # 1. Check presence & contents of required files.
    for file_path, expected_content in EXPECTED_TEMPLATES.items():
        assert file_path.exists(), f"Required file {file_path} is missing."
        assert file_path.is_file(), f"{file_path} exists but is not a regular file."
        actual_content = _read_text(file_path)
        assert actual_content == expected_content, (
            f"Contents of {file_path} do not match the expected initial data."
        )

    # 2. Ensure there are no additional *.template files.
    discovered_templates = {
        p for p in TEMPLATES_ROOT.rglob("*.template") if p.is_file()
    }
    extra = discovered_templates - EXPECTED_TEMPLATES.keys()
    missing = EXPECTED_TEMPLATES.keys() - discovered_templates
    assert not missing, (
        "The following required template files are missing: "
        + ", ".join(map(str, missing))
    )
    assert not extra, (
        "Unexpected *.template files found: "
        + ", ".join(map(str, extra))
    )


def test_no_output_directory_yet():
    """
    The student task is expected to create /home/user/provision/output/.
    Prior to execution, that directory must not exist.
    """
    assert not OUTPUT_DIR.exists(), (
        f"Directory {OUTPUT_DIR} already exists — the environment is not clean."
    )


def test_no_archive_yet():
    """The final archive must not pre-exist."""
    assert not ARCHIVE_PATH.exists(), (
        f"Archive {ARCHIVE_PATH} already exists — the environment is not clean."
    )


def test_no_build_log_yet():
    """The build.log must not pre-exist."""
    assert not BUILD_LOG.exists(), (
        f"Log file {BUILD_LOG} already exists — the environment is not clean."
    )


def test_templates_permissions_are_readable():
    """Ensure that the template files are at least readable by the current user."""
    for path in EXPECTED_TEMPLATES:
        assert os.access(path, os.R_OK), f"Template file {path} is not readable."