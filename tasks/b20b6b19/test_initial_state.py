# test_initial_state.py
#
# This pytest suite confirms that the *starting* filesystem state
# contains the expected source material for the scraping task and
# nothing basic is missing.  It deliberately stays away from any
# of the output artefacts the student will create later.

import re
from pathlib import Path

import pytest

PAGES_DIR = Path("/home/user/website/pages")
EXPECTED_FILES = {
    PAGES_DIR / "page1.html",
    PAGES_DIR / "page2.html",
    PAGES_DIR / "page3.html",
}

TABLE_ID_PATTERN = re.compile(r'<table[^>]+id=["\']weather["\']', re.IGNORECASE)
HEADER_PATTERN = re.compile(
    r"<tr>\s*<th>\s*Date\s*</th>\s*<th>\s*Temperature\s*</th>\s*<th>\s*Humidity\s*</th>\s*</tr>",
    re.IGNORECASE | re.DOTALL,
)


def read_file_text(path: Path) -> str:
    """Return file content as text; raises helpful error if unreadable."""
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read file {path}: {exc}")


def test_pages_directory_exists_and_is_readable():
    assert PAGES_DIR.exists(), f"Required directory {PAGES_DIR} is missing."
    assert PAGES_DIR.is_dir(), f"{PAGES_DIR} exists but is not a directory."
    # Check we can list its contents
    try:
        _ = list(PAGES_DIR.iterdir())
    except PermissionError as exc:  # pragma: no cover
        pytest.fail(f"Cannot access directory listing of {PAGES_DIR}: {exc}")


def test_expected_html_files_present():
    found = {p for p in PAGES_DIR.glob("*.html")}
    missing = EXPECTED_FILES - found
    extras = found - EXPECTED_FILES
    assert not missing, f"The following expected HTML files are missing: {sorted(missing)}"
    # Warn (but do not fail) if other HTML files are present – they won't be parsed in tests.
    if extras:  # pragma: no cover
        pytest.xfail(f"Extra HTML files detected in {PAGES_DIR}: {sorted(extras)}")


@pytest.mark.parametrize("html_path", sorted(EXPECTED_FILES))
def test_each_html_contains_weather_table(html_path: Path):
    text = read_file_text(html_path)
    assert TABLE_ID_PATTERN.search(
        text
    ), f"{html_path} does not contain a table with id='weather'."


@pytest.mark.parametrize("html_path", sorted(EXPECTED_FILES))
def test_each_html_contains_correct_header_row(html_path: Path):
    text = read_file_text(html_path)
    assert HEADER_PATTERN.search(
        text
    ), (
        f"{html_path} is missing the exact header row "
        "'Date', 'Temperature', 'Humidity' in that order."
    )