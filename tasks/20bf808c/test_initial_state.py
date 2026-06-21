# test_initial_state.py
#
# Pytest suite that validates the initial operating-system / filesystem
# state **before** the student performs any of the required actions.
#
# What is checked:
#   1. Presence of the three reference configuration files in
#      /home/user/source_configs/ with the expected key contents.
#   2. Presence (and emptiness) of the destination directory
#      /home/user/remote_share/site_backup/.
#   3. Presence (and emptiness) of the writable logs directory
#      /home/user/logs/.
#
# Nothing related to the *output* artefacts that the student is supposed
# to create (ping / rsync logs, copied files, …) is tested here – this
# suite only confirms the starting conditions.

from pathlib import Path
import pytest

HOME = Path("/home/user")

SOURCE_DIR      = HOME / "source_configs"
REMOTE_DIR      = HOME / "remote_share" / "site_backup"
LOGS_DIR        = HOME / "logs"

EXPECTED_CONFIGS = {
    "router1.conf": {
        "hostname": "Router1",
        "ip_part":  "10.0.1.1",
    },
    "router2.conf": {
        "hostname": "Router2",
        "ip_part":  "10.0.2.1",
    },
    "router3.conf": {
        "hostname": "Router3",
        "ip_part":  "10.0.3.1",
    },
}

###############################################################################
# Helper functions
###############################################################################
def read_text_strict(path: Path) -> str:
    """
    Return file content as UTF-8 text.  If the file cannot be read as UTF-8
    the test will fail with a clear message.
    """
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Unable to read {path} as UTF-8 text: {exc}", pytrace=False)

###############################################################################
# Tests for /home/user/source_configs/
###############################################################################
def test_source_directory_present_and_has_only_expected_files():
    assert SOURCE_DIR.is_dir(), f"Directory {SOURCE_DIR} is missing."

    found_files = sorted(p.name for p in SOURCE_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_CONFIGS.keys())
    assert found_files == expected_files, (
        f"{SOURCE_DIR} should contain exactly the files "
        f"{expected_files}, but found {found_files}."
    )

@pytest.mark.parametrize("filename,expect", EXPECTED_CONFIGS.items())
def test_each_config_file_contains_expected_strings(filename, expect):
    file_path = SOURCE_DIR / filename
    content = read_text_strict(file_path)

    # Ensure hostname line is present
    assert f"hostname {expect['hostname']}" in content, (
        f"{file_path} does not contain the expected "
        f"'hostname {expect['hostname']}' line."
    )

    # Ensure interface line is present (generic, same for all)
    assert "interface Gig0/0/0" in content, (
        f"{file_path} does not contain the expected 'interface Gig0/0/0' line."
    )

    # Ensure correct IP address line is present
    assert expect["ip_part"] in content, (
        f"{file_path} does not contain the expected IP address "
        f"'{expect['ip_part']}'."
    )

###############################################################################
# Tests for /home/user/remote_share/site_backup/
###############################################################################
def test_remote_directory_present_and_empty():
    assert REMOTE_DIR.is_dir(), f"Directory {REMOTE_DIR} is missing."

    contents = list(REMOTE_DIR.iterdir())
    assert contents == [], (
        f"{REMOTE_DIR} is expected to be empty at task start, "
        f"but contains: {[p.name for p in contents]}"
    )

###############################################################################
# Tests for /home/user/logs/
###############################################################################
def test_logs_directory_present_and_empty():
    assert LOGS_DIR.is_dir(), f"Directory {LOGS_DIR} is missing."

    contents = list(LOGS_DIR.iterdir())
    # We explicitly do NOT check for (non-)existence of the files that
    # will be created later; we only assert that nothing is present *yet*.
    assert contents == [], (
        f"{LOGS_DIR} should be empty before the student runs any commands, "
        f"but contains: {[p.name for p in contents]}"
    )