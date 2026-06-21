# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system state
# BEFORE the student performs any action.
#
# It checks that:
#   • /home/user/configs exists and is a directory.
#   • /home/user/configs/httpd.conf.prev exists with the exact expected
#     contents (including a trailing newline).
#   • /home/user/configs/httpd.conf.curr exists with the exact expected
#     contents (including a trailing newline).
#
# NOTE: Per the authoring guidelines we deliberately do *not* test for the
#       presence or absence of the student-created output file
#       (/home/user/configs/added_lines.log).

import pathlib
import textwrap

import pytest


CONFIG_DIR = pathlib.Path("/home/user/configs")
PREV_FILE = CONFIG_DIR / "httpd.conf.prev"
CURR_FILE = CONFIG_DIR / "httpd.conf.curr"


@pytest.fixture(scope="module")
def expected_prev_lines():
    return [
        "# Apache HTTPD previous config",
        'ServerRoot "/etc/httpd"',
        "Listen 80",
        "Include conf.modules.d/*.conf",
        "User apache",
        "Group apache",
    ]


@pytest.fixture(scope="module")
def expected_curr_lines():
    return [
        "# Apache HTTPD current config",
        'ServerRoot "/etc/httpd"',
        "Listen 80",
        "Listen 8080",
        "Include conf.modules.d/*.conf",
        "User apache",
        "Group apache",
    ]


def _read_lines(path: pathlib.Path):
    """
    Read a file and return a tuple:
        (list_of_lines_without_newline_char, raw_text)
    Raises an assertion error with a helpful message if the file is missing.
    """
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."
    raw_text = path.read_text(encoding="utf-8")
    lines = raw_text.splitlines()
    return lines, raw_text


def test_config_directory_exists():
    assert CONFIG_DIR.exists(), (
        f"Directory {CONFIG_DIR} is missing. "
        "The initial exercise setup should include this directory."
    )
    assert CONFIG_DIR.is_dir(), f"{CONFIG_DIR} exists but is not a directory."


def test_prev_file_contents(expected_prev_lines):
    lines, raw_text = _read_lines(PREV_FILE)

    # Check trailing newline
    assert raw_text.endswith(
        "\n"
    ), f"{PREV_FILE} must end with a single trailing newline character."

    # Check line-by-line content
    assert lines == expected_prev_lines, (
        f"The contents of {PREV_FILE} do not match the expected initial state.\n"
        "Expected:\n"
        + textwrap.indent("\n".join(expected_prev_lines), prefix="    ")
        + "\n\nFound:\n"
        + textwrap.indent("\n".join(lines), prefix="    ")
    )


def test_curr_file_contents(expected_curr_lines):
    lines, raw_text = _read_lines(CURR_FILE)

    # Check trailing newline
    assert raw_text.endswith(
        "\n"
    ), f"{CURR_FILE} must end with a single trailing newline character."

    # Check line-by-line content
    assert lines == expected_curr_lines, (
        f"The contents of {CURR_FILE} do not match the expected initial state.\n"
        "Expected:\n"
        + textwrap.indent("\n".join(expected_curr_lines), prefix="    ")
        + "\n\nFound:\n"
        + textwrap.indent("\n".join(lines), prefix="    ")
    )