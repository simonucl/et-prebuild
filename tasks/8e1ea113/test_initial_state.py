# test_initial_state.py
#
# This pytest suite validates the initial filesystem state that must be
# present *before* the student carries out the deployment-log task.
#
# It checks only the provided release artefacts under
#   /home/user/deploy/releases/
# and deliberately ignores anything that will be created later in
#   /home/user/deploy/logs/
#
# If any assertion fails, the emitted message pin-points exactly what is
# missing or malformed so that the student can fix the setup before
# attempting the transformation steps.

import pathlib
import pytest

# ---------------------------------------------------------------------------
# Constants describing the expected initial state
# ---------------------------------------------------------------------------

RELEASE_ROOT = pathlib.Path("/home/user/deploy/releases")

EXPECTED_RELEASES = {
    "v2.3.1": {
        "date": "2023-04-17",
        "headline": "Fixed issue with authentication timeout",
    },
    "v2.4.0": {
        "date": "2023-05-29",
        "headline": "Added support for PostgreSQL 14",
    },
    "v2.4.1": {
        "date": "2023-06-12",
        "headline": "Hotfix: Corrected SQL migration script for user_profiles table",
    },
}

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _load_release_notes(version: str) -> list[str]:
    """
    Read the release_notes.md file for *version* and return a list of stripped
    lines (no trailing newline characters).
    """
    file_path = RELEASE_ROOT / version / "release_notes.md"
    assert file_path.is_file(), (
        f"Expected release notes file not found: {file_path}. "
        "Ensure the file exists before running the task."
    )
    with file_path.open(encoding="utf-8") as fp:
        return [line.rstrip("\n") for line in fp]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_release_directory_exists():
    """
    Verify that the /home/user/deploy/releases directory exists.
    """
    assert RELEASE_ROOT.is_dir(), (
        f"Missing directory: {RELEASE_ROOT}. "
        "The initial release artefacts must be located here."
    )


@pytest.mark.parametrize("version", EXPECTED_RELEASES.keys())
def test_individual_release_structure(version):
    """
    For each expected semantic version, ensure its directory and markdown file
    exist.
    """
    dir_path = RELEASE_ROOT / version
    file_path = dir_path / "release_notes.md"

    assert dir_path.is_dir(), (
        f"Missing release directory: {dir_path}. "
        "All provided versions must exist before transformation."
    )
    assert file_path.is_file(), (
        f"Missing file: {file_path}. "
        "Each release directory must contain a release_notes.md file."
    )


@pytest.mark.parametrize(
    "version,expected",
    [(v, EXPECTED_RELEASES[v]) for v in EXPECTED_RELEASES],
)
def test_release_notes_content(version, expected):
    """
    Validate the contents of each release_notes.md file:

    1. First non-empty line == '# Release {version}'
    2. Line starting with 'Date: ' contains the expected date
    3. Very first bullet line (starts with '- ') matches the expected headline
    """
    lines = [ln for ln in _load_release_notes(version) if ln.strip()]
    assert lines, (
        f"File {version}/release_notes.md is empty. "
        "It must contain at least a title, date, and one bullet line."
    )

    # 1. Title line
    expected_title = f"# Release {version}"
    assert lines[0] == expected_title, (
        f"{version}/release_notes.md: "
        f"first line should be '{expected_title}' but found '{lines[0]}'."
    )

    # 2. Date line
    date_lines = [ln for ln in lines if ln.startswith("Date: ")]
    assert date_lines, (
        f"{version}/release_notes.md: missing 'Date: ' line."
    )
    actual_date_line = date_lines[0]
    actual_date = actual_date_line.removeprefix("Date: ").strip()
    assert actual_date == expected["date"], (
        f"{version}/release_notes.md: expected date '{expected['date']}' "
        f"but found '{actual_date}'."
    )

    # 3. First bullet (headline)
    bullet_lines = [ln for ln in lines if ln.lstrip().startswith("- ")]
    assert bullet_lines, (
        f"{version}/release_notes.md: no bullet points found."
    )
    actual_headline = bullet_lines[0].lstrip()[2:].strip()  # remove '- '
    assert (
        actual_headline == expected["headline"]
    ), (
        f"{version}/release_notes.md: expected headline "
        f"'{expected['headline']}' but found '{actual_headline}'."
    )