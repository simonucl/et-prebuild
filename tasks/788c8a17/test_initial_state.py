# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem
# before the student performs any actions.  It confirms that the two
# existing configuration files are present at the expected absolute
# paths and that their contents match the provided “STARTING STATE”
# verbatim (ignoring only the trailing newline that many editors add).
#
# If any assertion fails, the error message clearly states what is
# missing or differs, guiding the student to the exact problem.
#
# NOTE:
# • We deliberately DO NOT check for /home/user/update_report.txt
#   or for any other “output” artefacts, as those belong to the
#   *final* state and must not exist yet.

from pathlib import Path
import pytest

HOME = Path("/home/user")

# ----------------------------------------------------------------------
# Helper utilities
# ----------------------------------------------------------------------
def read_file_lines(path: Path):
    """
    Read a text file and return a list of lines without their trailing
    newline characters.  Using .rstrip('\n') allows the test to pass
    regardless of whether the last line ends with an extra newline.
    """
    return [line.rstrip("\n") for line in path.read_text(encoding="utf-8").splitlines()]


# ----------------------------------------------------------------------
# Expected initial contents
# ----------------------------------------------------------------------
EXPECTED_YAML_LINES = [
    "version: 1.0",
    "debug: false",
    "database:",
    "  host: localhost",
    "  port: 5432",
]

EXPECTED_TOML_LINES = [
    "[server]",
    "port = 9000",
    "",
    "[logging]",
    'level = "debug"',
]

# ----------------------------------------------------------------------
# Tests
# ----------------------------------------------------------------------
def test_directories_exist():
    """Base directories required by the starting state must exist."""
    yaml_dir = HOME / "webapp" / "config"
    toml_dir = HOME / "monitor"

    for d in (yaml_dir, toml_dir):
        assert d.is_dir(), f"Required directory is missing: {d}"


def test_settings_yaml_exists_and_content():
    """/home/user/webapp/config/settings.yaml must exist and match the expected starting content."""
    yaml_path = HOME / "webapp" / "config" / "settings.yaml"
    assert yaml_path.is_file(), f"File not found: {yaml_path}"

    lines = read_file_lines(yaml_path)
    assert (
        lines == EXPECTED_YAML_LINES
    ), (
        f"{yaml_path} does not match the expected initial content.\n"
        f"Expected:\n{EXPECTED_YAML_LINES}\n\nFound:\n{lines}"
    )


def test_service_toml_exists_and_content():
    """/home/user/monitor/service.toml must exist and match the expected starting content."""
    toml_path = HOME / "monitor" / "service.toml"
    assert toml_path.is_file(), f"File not found: {toml_path}"

    lines = read_file_lines(toml_path)
    assert (
        lines == EXPECTED_TOML_LINES
    ), (
        f"{toml_path} does not match the expected initial content.\n"
        f"Expected:\n{EXPECTED_TOML_LINES}\n\nFound:\n{lines}"
    )