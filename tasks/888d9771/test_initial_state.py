# test_initial_state.py
#
# This pytest suite verifies the initial state of the workstation **before**
# the student adds the security-scan automation.  It confirms that the
# web-application project files exist and contain the exact “insecure” code
# snippets that the forthcoming task must detect.
#
# IMPORTANT:  Per the instructions, this file intentionally does *not* check
# for the presence or absence of the expected output directory or log file
# (/home/user/security_reports/…), because those are artifacts the student
# is supposed to create.

import pathlib
import pytest

# Base paths used throughout the tests
WEBAPP_ROOT = pathlib.Path("/home/user/projects/webapp")
APP_PY = WEBAPP_ROOT / "app.py"
HELPERS_PY = WEBAPP_ROOT / "utils" / "helpers.py"
README_MD = WEBAPP_ROOT / "README.md"


def _read_file(path: pathlib.Path) -> str:
    """Utility: read file content, raising a helpful assertion message if the
    file is missing."""
    assert path.exists(), f"Required file not found: {path}"
    return path.read_text(encoding="utf-8")


def test_project_directory_exists():
    """The main project directory must exist."""
    assert WEBAPP_ROOT.is_dir(), f"Directory missing: {WEBAPP_ROOT}"


def test_expected_python_files_exist():
    """Required Python source files must be present."""
    assert APP_PY.is_file(), f"Missing expected Python file: {APP_PY}"
    assert HELPERS_PY.is_file(), f"Missing expected Python file: {HELPERS_PY}"


def test_readme_exists():
    """README is part of the starting repository layout."""
    assert README_MD.is_file(), f"Missing README file: {README_MD}"


@pytest.mark.parametrize(
    "path, expected_snippets",
    [
        (
            APP_PY,
            [
                'os.system("ls -la")  # insecure',
                'eval("2+2")  # insecure',
            ],
        ),
        (
            HELPERS_PY,
            [
                "subprocess.call(cmd, shell=True)  # insecure",
            ],
        ),
    ],
)
def test_insecure_snippets_present(path, expected_snippets):
    """
    Each source file must already contain the *exact* insecure code snippets
    specified in the task description.  These are what the student’s script
    will search for, so their absence would invalidate the assignment.
    """
    content = _read_file(path)
    for snippet in expected_snippets:
        assert (
            snippet in content
        ), f"Expected snippet not found in {path}:\n    {snippet!r}"


def test_app_py_complete_content():
    """
    Confirm that /home/user/projects/webapp/app.py matches the known reference
    content byte-for-byte.  This guards against accidental modifications to
    the starter code.
    """
    expected = (
        "# main application\n"
        "import os\n"
        "def run():\n"
        '    os.system("ls -la")  # insecure\n'
        '    print("Hello")\n'
        '    eval("2+2")  # insecure\n'
    )
    actual = _read_file(APP_PY)
    assert (
        actual == expected
    ), (
        f"{APP_PY} content does not match the expected starter file.\n"
        "----- Expected -----\n"
        f"{expected}\n"
        "----- Actual -----\n"
        f"{actual}\n"
        "--------------------"
    )


def test_helpers_py_complete_content():
    """
    Confirm that /home/user/projects/webapp/utils/helpers.py matches the known
    reference content.
    """
    expected = (
        "import subprocess\n"
        "def dangerous(cmd):\n"
        "    subprocess.call(cmd, shell=True)  # insecure\n"
        "def safe():\n"
        '    print("safe")\n'
    )
    actual = _read_file(HELPERS_PY)
    assert (
        actual == expected
    ), (
        f"{HELPERS_PY} content does not match the expected starter file.\n"
        "----- Expected -----\n"
        f"{expected}\n"
        "----- Actual -----\n"
        f"{actual}\n"
        "--------------------"
    )