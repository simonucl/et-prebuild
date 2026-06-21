# test_initial_state.py
#
# This pytest suite verifies the workspace *before* the student performs
# any actions for the “Organize project files and generate a simple
# security-scan report” task.
#
# IMPORTANT:  Do NOT add tests that reference paths the student is
# expected to create as part of the assignment (e.g. /home/user/workspace/my_app/*).
# We only validate the starting conditions.

import pathlib
import pytest

HOME = pathlib.Path("/home/user")
WORKSPACE = HOME / "workspace"
UNORGANIZED_DIR = WORKSPACE / "unorganized"

# Absolute paths for the files that must exist at the start.
SECRET_PY = UNORGANIZED_DIR / "secret.py"
CONFIG_JS = UNORGANIZED_DIR / "config.js"
README_MD = UNORGANIZED_DIR / "readme.md"

@pytest.fixture(scope="session")
def unorganized_dir():
    """Return pathlib.Path for the unorganized directory, asserting it exists."""
    assert UNORGANIZED_DIR.exists(), (
        f"The required directory {UNORGANIZED_DIR} is missing. "
        "The workspace should start with this directory already present."
    )
    assert UNORGANIZED_DIR.is_dir(), (
        f"{UNORGANIZED_DIR} exists but is not a directory."
    )
    return UNORGANIZED_DIR


def test_required_files_exist(unorganized_dir):
    """Verify that the three expected files are present inside the unorganized dump."""
    for file_path in (SECRET_PY, CONFIG_JS, README_MD):
        assert file_path.exists(), (
            f"The file {file_path} is expected to be present at the start but was not found."
        )
        assert file_path.is_file(), f"{file_path} exists but is not a regular file."


def test_secret_py_contains_expected_secret():
    """secret.py must contain the exact SECRET_KEY assignment."""
    expected_line = 'SECRET_KEY="p@ssw0rd123"'
    try:
        content = SECRET_PY.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        pytest.skip(f"{SECRET_PY} is missing; existence is checked in another test.")

    assert any(expected_line in line for line in content), (
        f'{SECRET_PY} should contain the exact line:\n    {expected_line}\n'
        "but it was not found."
    )


def test_config_js_contains_expected_secret():
    """config.js must contain the expected secret key constant."""
    expected_line = 'const SECRET_KEY="xyz-999";'
    try:
        content = CONFIG_JS.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        pytest.skip(f"{CONFIG_JS} is missing; existence is checked in another test.")

    assert any(expected_line in line for line in content), (
        f'{CONFIG_JS} should contain the exact line:\n    {expected_line}\n'
        "but it was not found."
    )


def test_readme_md_is_nonempty():
    """Ensure readme.md exists and is not empty (basic sanity check)."""
    try:
        text = README_MD.read_text(encoding="utf-8")
    except FileNotFoundError:
        pytest.skip(f"{README_MD} is missing; existence is checked in another test.")

    assert text.strip(), f"{README_MD} is empty, but it should contain initial notes."