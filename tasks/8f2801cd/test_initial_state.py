# test_initial_state.py
#
# This pytest suite verifies that the *starting* operating-system / filesystem
# state required for the exercise is present **before** the student writes any
# code.  It intentionally does NOT look for the artefacts that students are
# asked to create later (e.g. the output directory or JSON file).

import pathlib
import textwrap

ROOT_DIR = pathlib.Path("/home/user")
SRE_MONITOR_DIR = ROOT_DIR / "sre_monitor"
CONFIG_DIR = SRE_MONITOR_DIR / "config"
INI_FILE = CONFIG_DIR / "services.ini"

# The exact INI content expected to be pre-seeded on disk.
EXPECTED_INI_CONTENT = textwrap.dedent(
    """
    [web]
    name = frontend
    host = 127.0.0.1
    port = 80

    [db]
    name = database
    host = 127.0.0.1
    port = 5432

    [external_dns]
    name = google_dns
    host = 8.8.8.8
    port = 53
    """
).lstrip("\n").splitlines()  # list of lines for robust comparison


def test_root_directory_exists():
    assert ROOT_DIR.is_dir(), f"Expected directory {ROOT_DIR} is missing"


def test_sre_monitor_directory_exists():
    assert SRE_MONITOR_DIR.is_dir(), (
        f"Expected directory {SRE_MONITOR_DIR} does not exist. "
        "The exercise requires this as the project root."
    )


def test_config_directory_exists():
    assert CONFIG_DIR.is_dir(), (
        f"Expected directory {CONFIG_DIR} is missing. "
        "It should contain the pre-seeded services.ini file."
    )


def test_services_ini_exists():
    assert INI_FILE.is_file(), (
        f"Required INI file {INI_FILE} is missing. "
        "The exercise cannot proceed without this configuration."
    )


def test_services_ini_contents_are_correct():
    """
    Verify that /home/user/sre_monitor/config/services.ini is present
    and its contents match the exact expected starting template.
    The comparison is done line-by-line to tolerate the optional
    presence or absence of a final trailing newline.
    """
    ini_lines = INI_FILE.read_text().splitlines()
    assert ini_lines == EXPECTED_INI_CONTENT, (
        f"Contents of {INI_FILE} do not match the expected template.\n\n"
        "Expected:\n"
        + "\n".join(EXPECTED_INI_CONTENT)
        + "\n\nActual:\n"
        + "\n".join(ini_lines)
    )