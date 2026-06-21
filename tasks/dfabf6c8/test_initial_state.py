# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state
# (before the student makes any changes) is exactly as described in
# the task.  If a test here fails, the environment is not set up
# correctly for the student to proceed.

from pathlib import Path
import pytest

PROJECT_DIR = Path("/home/user/observability-dashboard")
VERSION_FILE = PROJECT_DIR / "VERSION"
CHANGELOG_FILE = PROJECT_DIR / "CHANGELOG.md"

EXPECTED_VERSION_CONTENT = "1.4.2\n"

# The en-dash (U+2013) is **required** in the third line.
EXPECTED_CHANGELOG_LINES = [
    "## [1.4.2] - 2023-04-27\n",
    "### Fixed\n",
    "– Corrected alert rule syntax in latency dashboard\n",
    "\n",
]


def _read_lines(path: Path):
    """
    Return a list with every line *including* its trailing newline
    character so we can compare byte-for-byte.
    """
    with path.open("r", encoding="utf-8", newline="") as fp:
        return fp.readlines()


def test_project_directory_exists():
    assert PROJECT_DIR.is_dir(), (
        f"Expected project directory '{PROJECT_DIR}' to exist, "
        "but it is missing."
    )


def test_version_file_initial_state():
    assert VERSION_FILE.is_file(), (
        f"Expected VERSION file at '{VERSION_FILE}' but it was not found."
    )

    content = VERSION_FILE.read_text(encoding="utf-8")
    assert content == EXPECTED_VERSION_CONTENT, (
        "VERSION file has unexpected content.\n"
        f"Expected exactly: {repr(EXPECTED_VERSION_CONTENT)}\n"
        f"Actual content : {repr(content)}"
    )


def test_changelog_initial_state():
    assert CHANGELOG_FILE.is_file(), (
        f"Expected CHANGELOG at '{CHANGELOG_FILE}' but it was not found."
    )

    lines = _read_lines(CHANGELOG_FILE)

    # Check that at least the first four lines are present
    assert len(lines) >= 4, (
        f"CHANGELOG.md should have at least 4 lines, "
        f"but it only has {len(lines)}."
    )

    # Compare the first four lines one-to-one
    for idx, (expected, actual) in enumerate(zip(EXPECTED_CHANGELOG_LINES, lines[:4]), 1):
        assert actual == expected, (
            f"Line {idx} of CHANGELOG.md is incorrect.\n"
            f"Expected: {repr(expected)}\n"
            f"Actual  : {repr(actual)}"
        )

    # Optional: ensure the new 1.5.0 header is NOT yet present
    assert "## [1.5.0]" not in "".join(lines), (
        "CHANGELOG.md already contains a 1.5.0 section, "
        "but the student has not performed the bump yet."
    )