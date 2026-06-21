# test_initial_state.py
#
# This test-suite verifies that the repository is in its ORIGINAL state
# *before* the student runs any commands.  It intentionally checks for
# the pre-existing version (1.4.2) and for the exact top-of-file layout
# of CHANGELOG.md.  If any of these assertions fail it means the starting
# point is already wrong, so the grader should stop immediately.

import pathlib
import pytest

APP_DIR = pathlib.Path("/home/user/app")
VERSION_FILE = APP_DIR / "version.txt"
CHANGELOG_FILE = APP_DIR / "CHANGELOG.md"


@pytest.fixture(scope="module")
def version_text():
    """Return the full contents of version.txt as bytes and str."""
    if not VERSION_FILE.is_file():
        pytest.fail(f"Required file missing: {VERSION_FILE}")
    data = VERSION_FILE.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{VERSION_FILE} is not valid UTF-8: {exc}")
    return text


@pytest.fixture(scope="module")
def changelog_lines():
    """Return CHANGELOG.md split into original text lines."""
    if not CHANGELOG_FILE.is_file():
        pytest.fail(f"Required file missing: {CHANGELOG_FILE}")
    try:
        content = CHANGELOG_FILE.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{CHANGELOG_FILE} is not valid UTF-8: {exc}")
    return content.splitlines()  # keep exact text (no trailing '\n')


def test_version_file_contents(version_text):
    """version.txt must contain exactly '1.4.2\\n'."""
    assert version_text == "1.4.2\n", (
        f"{VERSION_FILE} should contain exactly '1.4.2' followed by a single "
        f"newline. Found: {repr(version_text)}"
    )
    assert "1.4.3" not in version_text, (
        "version.txt already contains 1.4.3 – initial state must be 1.4.2."
    )


def test_changelog_header(changelog_lines):
    """
    The first non-empty lines of CHANGELOG.md must correspond to version 1.4.2,
    i.e. the new 1.4.3 entry must NOT yet exist in the initial state.
    """
    # Filter out empty lines while preserving order/index.
    non_empty = [ln for ln in changelog_lines if ln.strip() != ""]

    expected = [
        "## [1.4.2] - 2023-08-30",
        "### Fixed",
        "- Improved timeout handling for external API requests.",
        "## [1.4.1] - 2023-08-12",
    ]

    # We compare only the first 4 non-empty lines because the rest is not needed
    # for proving the initial state.
    assert non_empty[:4] == expected, (
        "CHANGELOG.md is not in its expected initial state. "
        f"First non-empty lines found: {non_empty[:4]!r}, expected: {expected!r}"
    )

    # Make sure the NEW entry is not already present.
    forbidden_header = "## [1.4.3] - 2023-09-14"
    assert forbidden_header not in changelog_lines, (
        f"Unexpected header '{forbidden_header}' already present in "
        f"{CHANGELOG_FILE}; CHANGELOG.md must start with 1.4.2 in the "
        f"initial state."
    )