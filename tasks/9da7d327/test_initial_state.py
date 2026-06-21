# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state required for the
“service audit” task **before** the student begins any work.

It checks only the input artefacts (configuration directory and the two INI
files).  It deliberately ignores anything in /home/user/support_ticket/report
because that is considered output for this exercise.

The tests will fail with clear explanations if something is missing or has
unexpected content/permissions.
"""
import configparser
import os
import stat
import textwrap
import pytest

HOME = "/home/user"
SUPPORT_DIR = os.path.join(HOME, "support_ticket")
CONFIG_DIR = os.path.join(SUPPORT_DIR, "configs")

APP1 = os.path.join(CONFIG_DIR, "app1.ini")
APP2 = os.path.join(CONFIG_DIR, "app2.ini")

EXPECTED_APP1_CONTENT = textwrap.dedent("""\
    [AuthService]
    enabled=true
    port=8080

    [DataCollector]
    enabled=true
    ; port intentionally omitted
    """)

EXPECTED_APP2_CONTENT = textwrap.dedent("""\
    [WebPortal]
    enabled=true
    port=8080

    [Metrics]
    enabled=false
    port=9100
    """)

def _strip_trailing_newlines(text: str) -> str:
    """
    Helper that removes any number of trailing newlines for robust comparison
    without disturbing intentional blank lines inside the file.
    """
    return text.rstrip("\n\r")

# --------------------------------------------------------------------------- #
# Filesystem structure & permissions                                          #
# --------------------------------------------------------------------------- #

def test_configs_directory_exists_and_permissions():
    assert os.path.isdir(CONFIG_DIR), (
        f"Required directory {CONFIG_DIR!r} is missing or not a directory."
    )
    mode = stat.S_IMODE(os.stat(CONFIG_DIR).st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"Directory {CONFIG_DIR!r} must have permissions 0o755 "
        f"but has 0o{mode:03o}."
    )

@pytest.mark.parametrize("path", [APP1, APP2])
def test_ini_files_exist_and_permissions(path):
    assert os.path.isfile(path), f"Required file {path!r} does not exist."
    mode = stat.S_IMODE(os.stat(path).st_mode)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"File {path!r} must have permissions 0o644 but has 0o{mode:03o}."
    )

# --------------------------------------------------------------------------- #
# File contents                                                               #
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize(
    "path, expected_raw",
    [
        (APP1, EXPECTED_APP1_CONTENT),
        (APP2, EXPECTED_APP2_CONTENT),
    ],
)
def test_ini_file_raw_content(path, expected_raw):
    """
    Ensure that each INI file matches EXACTLY the expected content, ignoring
    trailing newlines at the very end of the file.  This guards against
    accidental edits before the task starts.
    """
    with open(path, "r", encoding="utf-8") as fh:
        actual = fh.read()
    assert (
        _strip_trailing_newlines(actual) == _strip_trailing_newlines(expected_raw)
    ), (
        f"The contents of {path!r} differ from the expected initial state.\n"
        "If this file was modified, please restore it before starting the task."
    )

# --------------------------------------------------------------------------- #
# Semantic validation of the INI structure                                    #
# --------------------------------------------------------------------------- #

def _parse_ini(path: str) -> configparser.ConfigParser:
    cp = configparser.ConfigParser(comment_prefixes=(";"), strict=True, interpolation=None)
    with open(path, "r", encoding="utf-8") as fh:
        cp.read_file(fh)
    return cp

def test_app1_ini_semantics():
    cp = _parse_ini(APP1)

    # Expected sections
    assert set(cp.sections()) == {"AuthService", "DataCollector"}, (
        "app1.ini must contain only [AuthService] and [DataCollector] sections."
    )

    # [AuthService]
    assert cp.get("AuthService", "enabled") == "true"
    assert cp.getint("AuthService", "port") == 8080

    # [DataCollector]
    assert cp.get("DataCollector", "enabled") == "true"
    assert not cp.has_option("DataCollector", "port"), (
        "[DataCollector] in app1.ini should intentionally omit the 'port' key."
    )

def test_app2_ini_semantics():
    cp = _parse_ini(APP2)

    # Expected sections
    assert set(cp.sections()) == {"WebPortal", "Metrics"}, (
        "app2.ini must contain only [WebPortal] and [Metrics] sections."
    )

    # [WebPortal]
    assert cp.get("WebPortal", "enabled") == "true"
    assert cp.getint("WebPortal", "port") == 8080

    # [Metrics]
    assert cp.get("Metrics", "enabled") == "false"
    # Port is present but will not be relevant because enabled=false
    assert cp.getint("Metrics", "port") == 9100