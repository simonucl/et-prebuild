# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the support-case directory
# BEFORE the student performs any actions.  If one of these tests fails, it
# means the starting environment is already wrong and the assignment cannot be
# completed as described.
#
# IMPORTANT:  These tests purposefully assert the *pre-change* conditions:
#   • service.enabled is still false
#   • logging.level is still "info"
#   • There is NO [network] table in the TOML
#   • diag_report.log does NOT yet exist
#
# Only Python’s stdlib and pytest are used.

from pathlib import Path
import pytest
import re

SUPPORT_DIR = Path("/home/user/support_case")
YAML_FILE = SUPPORT_DIR / "app_config.yaml"
TOML_FILE = SUPPORT_DIR / "system_info.toml"
REPORT_FILE = SUPPORT_DIR / "diag_report.log"


def _read_text(path: Path) -> str:
    """Helper that returns file contents or raises a helpful pytest failure."""
    if not path.exists():
        pytest.fail(f"Expected file {path} to exist, but it is missing.")
    if not path.is_file():
        pytest.fail(f"Expected {path} to be a regular file, but it is not.")
    try:
        return path.read_text()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read file {path}: {exc}")


def test_support_directory_exists_and_is_directory():
    assert SUPPORT_DIR.exists(), f"Support directory {SUPPORT_DIR} does not exist."
    assert SUPPORT_DIR.is_dir(), f"{SUPPORT_DIR} exists but is not a directory."


def test_app_config_yaml_pre_change_state():
    content = _read_text(YAML_FILE)

    # Essential lines that **must** be present in the untouched YAML
    required_lines = [
        'service:',
        '  name: "FileProcessor"',
        '  version: "1.2.3"',
        '  enabled: false',
        '',
        'logging:',
        '  level: "info"',
        '  path: "/var/log/fileprocessor/"',
    ]

    for line in required_lines:
        assert line in content.splitlines(), (
            f'YAML file is missing expected line:\n    {line!r}\n'
            f"Current contents:\n{content}"
        )

    # Ensure the file has NOT yet been modified to the post-task state
    forbidden_patterns = [
        r"enabled:\s*true",
        r'level:\s*"debug"',
    ]
    for pattern in forbidden_patterns:
        assert not re.search(pattern, content), (
            f"YAML already appears modified; found pattern {pattern!r} in:\n{content}"
        )


def test_system_info_toml_pre_change_state():
    content = _read_text(TOML_FILE)

    # Basic sanity checks for existing tables
    for table in ("[cpu]", "[memory]", "[os]"):
        assert table in content, f"TOML file is missing expected table {table!r}."

    # Make sure no [network] table exists yet
    assert "[network]" not in content, (
        "TOML already contains a [network] table—this should only be added by the "
        "student during the exercise."
    )

    # Ensure ip/up keys are not prematurely present
    assert "ip = " not in content, "Found an unexpected 'ip =' key in system_info.toml."
    assert re.search(r"\bup\s*=", content) is None, (
        "Found an unexpected 'up =' key in system_info.toml."
    )


def test_diag_report_log_does_not_exist_yet():
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} already exists, but it should be created *after* the student "
        "performs the required steps."
    )