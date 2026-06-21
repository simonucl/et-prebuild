# test_initial_state.py
#
# This test-suite verifies that the operating-system is in the expected
# initial state *before* the student script is run.
#
# Checked items:
#   • /home/user/audit directory exists.
#   • /home/user/audit/server.cfg.orig exists and has the expected content.
#   • /home/user/audit/server.cfg.new  exists and has the expected content.
#
# The suite must not (and therefore does not) check for any of the files that
# the student is supposed to create, such as server.patch or server.cfg.patched.

from pathlib import Path
import pytest


AUDIT_DIR = Path("/home/user/audit")

# Expected file paths
ORIG_FILE = AUDIT_DIR / "server.cfg.orig"
NEW_FILE = AUDIT_DIR / "server.cfg.new"

# Expected contents with trailing newline
EXPECTED_ORIG_CONTENT = (
    "# Server configuration\n"
    "Port=8080\n"
    "EnableSSH=false\n"
    "MaxUsers=10\n"
)

EXPECTED_NEW_CONTENT = (
    "# Server configuration\n"
    "Port=2222\n"
    "EnableSSH=true\n"
    "MaxUsers=20\n"
    "Logging=verbose\n"
)


def _read_text(path: Path) -> str:
    """
    Helper that reads file contents as text, raising a useful assertion
    if the file cannot be read.
    """
    if not path.exists():
        pytest.fail(f"Expected file does not exist: {path}")
    if not path.is_file():
        pytest.fail(f"Expected a regular file, but found something else: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read file {path}: {exc}")


def test_audit_directory_exists():
    assert AUDIT_DIR.exists(), f"Directory missing: {AUDIT_DIR}"
    assert AUDIT_DIR.is_dir(), f"Path exists but is not a directory: {AUDIT_DIR}"


@pytest.mark.parametrize(
    "path, expected_content",
    [
        (ORIG_FILE, EXPECTED_ORIG_CONTENT),
        (NEW_FILE, EXPECTED_NEW_CONTENT),
    ],
)
def test_config_files_exist_with_correct_content(path: Path, expected_content: str):
    """
    Validate that each configuration file exists and matches exactly
    the expected baseline content (including trailing newline).
    """
    actual_content = _read_text(path)
    assert actual_content == expected_content, (
        f"Content of {path} does not match the expected baseline.\n"
        "Tip: check for missing or extra whitespace or newlines."
    )