# test_initial_state.py
#
# This pytest suite validates that the required **initial** filesystem
# state is present before the student performs any actions.  It checks
# only for the pre-existing resources and deliberately ignores all
# artefacts that the student is expected to create later.

import pathlib
import pytest

# ---- Constants ----------------------------------------------------------------

CONFIG_DIR = pathlib.Path("/home/user/project/config")

EXPECTED_FILES = {
    "app.conf": "[app]\nversion=1.2.3\nname=ExampleApp\n",
    "db.conf": (
        "[database]\n"
        "host=localhost\n"
        "port=5432\n"
        "user=admin\n"
        "pass=secret\n"
    ),
    "net.conf": (
        "[network]\n"
        "interface=eth0\n"
        "address=192.168.1.100\n"
    ),
}


# ---- Helper -------------------------------------------------------------------

def read_text(path: pathlib.Path) -> str:
    """Read a text file using UTF-8 and ensure it exists."""
    if not path.exists():
        pytest.fail(f"Expected file is missing: {path}")
    if not path.is_file():
        pytest.fail(f"Expected a regular file but found something else: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover – unlikely but defensive
        pytest.fail(f"Could not read {path}: {exc}")


# ---- Tests --------------------------------------------------------------------

def test_config_directory_exists():
    """The configuration directory must exist and be a directory."""
    assert CONFIG_DIR.exists(), f"Directory not found: {CONFIG_DIR}"
    assert CONFIG_DIR.is_dir(), f"Expected {CONFIG_DIR} to be a directory."


@pytest.mark.parametrize("filename, expected_content", EXPECTED_FILES.items())
def test_conf_files_exist_and_contents_match(filename, expected_content):
    """
    Each .conf file must exist inside the config directory and its
    contents must exactly match the expected baseline.
    """
    file_path = CONFIG_DIR / filename
    actual_content = read_text(file_path)

    assert (
        actual_content == expected_content
    ), (
        f"Contents of {file_path} do not match the expected baseline.\n"
        f"--- Expected ---\n{expected_content}\n"
        f"--- Actual ---\n{actual_content}\n"
        "Ensure the file has not been modified."
    )