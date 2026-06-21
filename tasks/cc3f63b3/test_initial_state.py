# test_initial_state.py
#
# This PyTest suite verifies that the starting filesystem state is exactly
# as expected *before* the student performs any actions.  It checks:
#
# 1. Presence of the required directories.
# 2. Presence and exact contents of the initial Python source files.
# 3. Absence of the yet-to-be-created scan_report.txt file.
#
# If any assertion fails, the accompanying message will describe the
# discrepancy so the student instantly knows what is missing or different.

import pathlib
import pytest

BASE_DIR = pathlib.Path("/home/user/security_scan")
SAMPLE_DIR = BASE_DIR / "sample_code"
REPORT_FILE = BASE_DIR / "scan_report.txt"


@pytest.fixture(scope="module")
def expected_files():
    """Return a mapping of absolute file paths to their exact expected contents."""
    return {
        SAMPLE_DIR / "app.py": (
            "# Sample app\n"
            "user_input = input(\"Enter expression: \")\n"
            "result = eval(user_input)  # insecure\n"
            "print(result)\n"
            "data = \"print('hello')\"\n"
            "eval(data)\n"
        ),
        SAMPLE_DIR / "utils.py": (
            "def calculate(expr):\n"
            "    return eval(expr)  # insecure\n"
        ),
    }


def test_directories_present():
    """Ensure the main and sample_code directories exist."""
    assert BASE_DIR.is_dir(), f"Required directory missing: {BASE_DIR}"
    assert SAMPLE_DIR.is_dir(), f"Required directory missing: {SAMPLE_DIR}"


def test_source_files_exist(expected_files):
    """Verify that every expected *.py file exists."""
    for path in expected_files:
        assert path.is_file(), f"Expected file not found: {path}"


@pytest.mark.parametrize("path,expected_content", [
    pytest.param(path, content, id=str(path))
    for path, content in {
        SAMPLE_DIR / "app.py": (
            "# Sample app\n"
            "user_input = input(\"Enter expression: \")\n"
            "result = eval(user_input)  # insecure\n"
            "print(result)\n"
            "data = \"print('hello')\"\n"
            "eval(data)\n"
        ),
        SAMPLE_DIR / "utils.py": (
            "def calculate(expr):\n"
            "    return eval(expr)  # insecure\n"
        ),
    }.items()
])
def test_source_file_contents(path, expected_content):
    """
    Ensure each source file's contents exactly match the truth value.
    The comparison is byte-for-byte (including trailing newlines).
    """
    actual = path.read_text(encoding="utf-8")
    assert actual == expected_content, (
        f"Contents of {path} differ from expected.\n"
        "---- Expected ----\n"
        f"{expected_content!r}\n"
        "---- Actual ----\n"
        f"{actual!r}\n"
    )


def test_report_file_absent():
    """
    The security scan report must NOT exist yet—students are expected to
    create it during the task.
    """
    assert not REPORT_FILE.exists(), (
        f"{REPORT_FILE} should not exist before running the student's solution."
    )