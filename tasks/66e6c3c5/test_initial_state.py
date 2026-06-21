# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state **before** the student’s solution is run.
#
# What we assert:
#   • The web-mirror directory and its expected files exist.
#   • targets.lst contains the exact three lines given in the spec.
#   • Each HTML file exists and contains key markers we will rely on later.
#   • No pre-existing output artefacts (/home/user/vulnscan and JSON file).
#
# If any of these assertions fail, the error message should make it crystal
# clear to the learner what is missing or unexpectedly present.
#
# Only stdlib + pytest are used.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
WEBMIRROR_DIR = HOME / "webmirror"
TARGETS_FILE = WEBMIRROR_DIR / "targets.lst"
VULNSCAN_DIR = HOME / "vulnscan"
REPORT_FILE = VULNSCAN_DIR / "vulnerability_report.json"


@pytest.fixture(scope="module")
def targets_contents():
    """Read targets.lst and return a list of stripped lines."""
    if not TARGETS_FILE.exists():
        pytest.skip(f"{TARGETS_FILE} is missing; cannot perform further checks.")
    # Keep trailing newline information for a dedicated test
    with TARGETS_FILE.open("rb") as fh:
        raw = fh.read()
    # Decode assuming UTF-8; if that fails the learner will see the traceback.
    text = raw.decode("utf-8")
    lines = text.splitlines(keepends=True)   # preserve newline characters
    stripped = [ln.rstrip("\r\n") for ln in lines]
    return stripped, lines


def test_webmirror_directory_exists():
    assert WEBMIRROR_DIR.is_dir(), (
        f"Expected directory {WEBMIRROR_DIR} to exist. "
        "This directory should contain the offline HTML mirror."
    )


def test_targets_file_exists_and_is_regular_file():
    assert TARGETS_FILE.is_file(), (
        f"Expected file {TARGETS_FILE} to exist and be a regular file."
    )


def test_targets_file_has_exact_three_entries(targets_contents):
    stripped, _ = targets_contents
    expected = ["site1.html", "site2.html", "site3.html"]
    assert stripped == expected, (
        f"{TARGETS_FILE} must contain exactly the lines:\n"
        f"{expected}\n"
        f"but the actual contents are:\n{stripped}"
    )


def test_targets_file_ends_with_newline(targets_contents):
    # The spec explicitly says “newline at the end of each line”.
    # Here we verify that the last raw line ends with '\n'.
    _, raw_lines = targets_contents
    assert raw_lines[-1].endswith("\n"), (
        f"{TARGETS_FILE} must end with a newline character "
        "so that each line, including the last, terminates properly."
    )


@pytest.mark.parametrize(
    "filename, must_contain_snippets",
    [
        (
            "site1.html",
            [
                'src="http://insecure.example.com/evil.js"',
                "eval(",
            ],
        ),
        (
            "site2.html",
            [
                'src="https://secure.example.com/safe.js"',
            ],
        ),
        (
            "site3.html",
            [
                'src="http://cdn.example.com/lib.js"',
                'src="http://bad.example.com/tracker.js"',
            ],
        ),
    ],
)
def test_each_html_file_exists_and_contains_expected_markers(
    filename, must_contain_snippets
):
    html_path = WEBMIRROR_DIR / filename
    assert html_path.is_file(), f"Expected HTML file {html_path} to exist."

    content = html_path.read_text(encoding="utf-8", errors="ignore")

    for snippet in must_contain_snippets:
        assert snippet in content, (
            f"Marker '{snippet}' not found in {html_path}. "
            "Initial HTML content does not match the specification."
        )


def test_vulnscan_directory_does_not_yet_exist():
    assert not VULNSCAN_DIR.exists(), (
        f"Directory {VULNSCAN_DIR} should NOT exist before the student "
        "runs their solution. It will be created by the script when needed."
    )


def test_report_file_does_not_yet_exist():
    assert not REPORT_FILE.exists(), (
        f"File {REPORT_FILE} should NOT exist before the student "
        "runs their solution."
    )