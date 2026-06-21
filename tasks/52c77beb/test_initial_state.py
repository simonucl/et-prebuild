# test_initial_state.py
"""
pytest suite that validates the *initial* filesystem/OS state for the
“observability-dashboard” version-bump exercise.

These tests assert that the starting point is exactly as the specification
describes *before* the student executes any command.
"""

import os
import stat
import textwrap

import pytest

ROOT = "/home/user/observability-dashboard"
VERSION_PATH = os.path.join(ROOT, "VERSION")
CHANGELOG_PATH = os.path.join(ROOT, "CHANGELOG.md")
LOG_PATH = os.path.join(ROOT, "version_bump.log")


def _read_file(path):
    """Utility that returns a file’s full content, raises an AssertionError with
    a clear message if the file cannot be read.
    """
    assert os.path.isfile(path), f"Expected file at {path!r} is missing."
    try:
        with open(path, "r", encoding="utf-8") as fp:
            return fp.read()
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path!r}: {exc}")


def test_root_directory_exists_and_writable():
    assert os.path.isdir(
        ROOT
    ), f"Required project root directory {ROOT!r} does not exist."

    # Basic writability check: user must have write permission bit.
    st_mode = os.stat(ROOT).st_mode
    user_writable = bool(st_mode & stat.S_IWUSR)
    assert (
        user_writable
    ), f"Project root directory {ROOT!r} must be writable by the user."


def test_version_file_initial_content():
    expected_content = "1.4.2\n"
    actual_content = _read_file(VERSION_PATH)
    assert (
        actual_content == expected_content
    ), textwrap.dedent(
        f"""\
        VERSION file content is incorrect.
        Expected exactly:
            {expected_content!r}
        Got:
            {actual_content!r}"""
    )


def test_changelog_initial_top_three_lines():
    expected_lines = [
        "## [1.4.2] - 2023-09-20\n",
        "### Added\n",
        "- Initial CPU saturation panel.\n",
    ]
    actual_lines = _read_file(CHANGELOG_PATH).splitlines(keepends=True)[:3]

    assert (
        actual_lines == expected_lines
    ), textwrap.dedent(
        f"""\
        CHANGELOG.md top three lines are not as expected.

        Expected (verbatim, including newlines and spacing):
        {''.join(expected_lines)!r}

        Got:
        {''.join(actual_lines)!r}
        """
    )


def test_version_bump_log_does_not_exist():
    assert not os.path.exists(
        LOG_PATH
    ), f"{LOG_PATH!r} should NOT exist at the initial state."