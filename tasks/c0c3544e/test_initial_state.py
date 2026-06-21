# test_initial_state.py
#
# This pytest suite validates that the *initial* operating-system / filesystem
# state is exactly as expected *before* the student writes any solution code.
#
# It checks ONLY the pre-existing configuration directory and files.
# It intentionally does NOT touch /home/user/incident_analysis/ or any
# output artefacts that the student will create later.

import pathlib
import textwrap
import pytest

HOME = pathlib.Path("/home/user")
CFG_DIR = HOME / "incident_configs"

# Expected INI files and their verbatim contents (no trailing spaces).
EXPECTED_FILES = {
    "service1.ini": textwrap.dedent(
        """\
        [network]
        port = 8080
        host = 0.0.0.0

        [auth]
        method = token

        [performance]
        debug_mode = false
        """
    ),
    "service2.ini": textwrap.dedent(
        """\
        [network]
        port = 65535
        host = 192.168.1.50

        [auth]
        method = none

        [performance]
        debug_mode = true
        """
    ),
    "service3.ini": textwrap.dedent(
        """\
        [network]
        port = 443
        host = 10.0.0.1

        [auth]
        method = oauth

        [performance]
        debug_mode = false
        """
    ),
}


@pytest.fixture(scope="module")
def cfg_path():
    """Return Path object for the configuration directory."""
    return CFG_DIR


def test_config_directory_exists(cfg_path):
    assert cfg_path.exists(), f"Directory {cfg_path} is missing."
    assert cfg_path.is_dir(), f"{cfg_path} exists but is not a directory."


def test_expected_ini_files_present(cfg_path):
    """All expected INI files must be present."""
    missing = [name for name in EXPECTED_FILES if not (cfg_path / name).is_file()]
    assert not missing, (
        "The following expected .ini files are missing in "
        f"{cfg_path}: {', '.join(missing)}"
    )


@pytest.mark.parametrize("filename,expected_content", EXPECTED_FILES.items())
def test_ini_file_contents_verbatim(cfg_path, filename, expected_content):
    """
    The contents of each INI file must match the specification exactly
    (ignoring a single trailing newline at EOF, which Git often adds).
    """
    file_path = cfg_path / filename
    assert file_path.is_file(), f"Expected file {file_path} is missing."

    actual = file_path.read_text()

    # Normalise: strip exactly one trailing newline if present to tolerate
    # POSIX text files, but otherwise compare verbatim.
    if actual.endswith("\n") and not expected_content.endswith("\n"):
        actual = actual[:-1]

    assert (
        actual == expected_content
    ), f"Contents of {file_path} do not match the expected specification."


def test_no_extra_ini_files(cfg_path):
    """Warn the student if unexpected .ini files are already present."""
    actual_files = {p.name for p in cfg_path.glob("*.ini")}
    unexpected = actual_files - EXPECTED_FILES.keys()
    assert not unexpected, (
        "Unexpected .ini files present in "
        f"{cfg_path}: {', '.join(sorted(unexpected))}. "
        "Please remove them before running the task."
    )