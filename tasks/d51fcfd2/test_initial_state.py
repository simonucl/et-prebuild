# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state for the
`clean-sensor-data` project *before* the student starts working.

The tests assert that:

1. The project directory exists.
2. VERSION file exists and still contains "0.2.1\n".
3. CHANGELOG.md exists, starts with "# Changelog", already contains
   a 0.2.1 section, and does *not* yet mention 0.2.2 or the new fix.
4. release_log.txt does **not** exist yet.

If any of these checks fail, the accompanying assertion message clearly
explains what is missing or unexpected.
"""
from pathlib import Path
import re
import pytest

BASE_DIR = Path("/home/user/projects/clean-sensor-data")
VERSION_PATH = BASE_DIR / "VERSION"
CHANGELOG_PATH = BASE_DIR / "CHANGELOG.md"
RELEASE_LOG_PATH = BASE_DIR / "release_log.txt"

@pytest.mark.describe("Project directory sanity checks")
def test_project_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected project directory {BASE_DIR} to exist, "
        "but it is missing. Did you clone/extract the project?"
    )

@pytest.mark.describe("VERSION file pre-check")
def test_version_file_pre_update():
    assert VERSION_PATH.is_file(), (
        f"VERSION file expected at {VERSION_PATH} but was not found."
    )

    content = VERSION_PATH.read_text(encoding="utf-8")
    assert content == "0.2.1\n", (
        "VERSION file should *initially* contain exactly '0.2.1\\n'.\n"
        f"Found content:\n{content!r}"
    )

@pytest.mark.describe("CHANGELOG.md pre-check")
def test_changelog_pre_update():
    assert CHANGELOG_PATH.is_file(), (
        f"CHANGELOG.md expected at {CHANGELOG_PATH} but was not found."
    )

    lines = CHANGELOG_PATH.read_text(encoding="utf-8").splitlines()

    # Filter out completely empty lines when looking for the header.
    non_empty_lines = [ln for ln in lines if ln.strip()]

    assert non_empty_lines, "CHANGELOG.md is empty."

    # 1. Check that the first non-empty line is '# Changelog'.
    first_line = non_empty_lines[0]
    assert first_line == "# Changelog", (
        "First non-empty line of CHANGELOG.md must be exactly '# Changelog'.\n"
        f"Found: {first_line!r}"
    )

    changelog_text = "\n".join(lines)

    # 2. Ensure the new version is NOT present yet.
    assert "## [0.2.2]" not in changelog_text, (
        "CHANGELOG.md already contains a 0.2.2 section, "
        "but this should be added by the student."
    )

    # 3. Ensure the old version 0.2.1 is present.
    assert re.search(r"^##\s*\[?0\.2\.1\]?", changelog_text, flags=re.MULTILINE), (
        "CHANGELOG.md must already include an entry for version 0.2.1."
    )

    # 4. Ensure the new fix line is NOT present yet.
    expected_fix_line = "Handle missing 'temperature' column gracefully (#23)"
    assert expected_fix_line not in changelog_text, (
        f"Found the line '{expected_fix_line}' in CHANGELOG.md already, "
        "but it should only appear after the student updates the file."
    )

@pytest.mark.describe("release_log.txt should not exist yet")
def test_release_log_absent():
    assert not RELEASE_LOG_PATH.exists(), (
        f"release_log.txt ({RELEASE_LOG_PATH}) should not exist before the task "
        "is performed."
    )