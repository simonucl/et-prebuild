# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state **before**
# the student carries out any actions required by the assignment.
#
# What we check (and only these things):
#   1. The project directory /home/user/projects/helloapp/ exists.
#   2. The template unit file
#        /home/user/projects/helloapp/helloapp.service.template
#      exists **and** still contains the two placeholder tokens
#      “@SCRIPT_PATH@” and “@ENV_PATH@”.
#   3. The application script
#        /home/user/projects/helloapp/helloapp.sh
#      exists and is executable.
#
# We deliberately do *not* inspect any of the files or directories that
# the student is supposed to create (/home/user/.config/…, the log file,
# etc.), in accordance with the testing rules.

import os
from pathlib import Path

PROJECT_DIR = Path("/home/user/projects/helloapp")
TEMPLATE_FILE = PROJECT_DIR / "helloapp.service.template"
SCRIPT_FILE = PROJECT_DIR / "helloapp.sh"

PLACEHOLDERS = {
    "@SCRIPT_PATH@",
    "@ENV_PATH@",
}


def _read_file(path: Path) -> str:
    """Helper that reads a text file using utf-8 and returns its content."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        raise AssertionError(f"Could not read {path}: {exc}") from exc


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Expected project directory {PROJECT_DIR} to exist, "
        "but it is missing."
    )


def test_template_file_present_and_contains_placeholders():
    assert TEMPLATE_FILE.is_file(), (
        "The template service unit is missing.\n"
        f"Expected to find: {TEMPLATE_FILE}"
    )

    content = _read_file(TEMPLATE_FILE)

    missing = [ph for ph in PLACEHOLDERS if ph not in content]
    assert not missing, (
        f"The template file {TEMPLATE_FILE} is expected to contain the "
        f"placeholder tokens {', '.join(PLACEHOLDERS)}, "
        f"but the following were not found: {', '.join(missing)}."
    )


def test_script_file_exists_and_is_executable():
    assert SCRIPT_FILE.is_file(), (
        "The application shell script is missing.\n"
        f"Expected to find: {SCRIPT_FILE}"
    )

    is_executable = os.access(SCRIPT_FILE, os.X_OK)
    assert is_executable, (
        f"The script {SCRIPT_FILE} exists but is not marked as executable. "
        "Run `chmod +x` on it before proceeding."
    )