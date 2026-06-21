# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state **before** the
# student performs any actions.  It checks only the pre-existing input
# structure and deliberately ignores any files or directories that the
# exercise asks the student to create (e.g. reports/ or logs/).
#
# Requirements verified:
#   • Project directory hierarchy exists.
#   • Exactly the expected two CSS files exist that match the glob
#     /home/user/project/assets/css/style_*.css.
#   • The contents of those two files are byte-for-byte correct.
#
# The tests are intentionally explicit so that, if a failure occurs,
# the error message clearly tells the learner what is missing or wrong.

import pathlib
import pytest

PROJECT_ROOT = pathlib.Path("/home/user/project")
ASSETS_DIR = PROJECT_ROOT / "assets"
CSS_DIR = ASSETS_DIR / "css"

STYLE_MAIN = CSS_DIR / "style_main.css"
STYLE_THEME = CSS_DIR / "style_theme.css"

# Expected file contents with Unix LF endings
EXPECTED_MAIN_CONTENT = (
    "body { background-color: #ff0000; color: #00ff00; }\n"
    "h1   { color: #ff0000; }\n"
    "p    { border: 1px solid #0000ff; }\n"
)

EXPECTED_THEME_CONTENT = (
    ".nav    { background: #ABC123; }\n"
    ".footer { background: #ff0000; }\n"
    ".btn    { background: #abc123; }\n"
    ".header { color: #FFF; }   /* 3-digit code must be ignored */\n"
)


def test_directory_structure_exists():
    """Verify that the required directory hierarchy exists."""
    assert PROJECT_ROOT.is_dir(), f"Missing directory: {PROJECT_ROOT}"
    assert ASSETS_DIR.is_dir(), f"Missing directory: {ASSETS_DIR}"
    assert CSS_DIR.is_dir(), f"Missing directory: {CSS_DIR}"


def test_css_files_exist():
    """Ensure the two expected CSS files exist."""
    for file_path in (STYLE_MAIN, STYLE_THEME):
        assert file_path.is_file(), f"Missing file: {file_path}"


def test_no_extra_style_css_files():
    """
    Confirm that the only files matching style_*.css are the two
    documented ones.  This guards against unintended extra files.
    """
    expected = {STYLE_MAIN.name, STYLE_THEME.name}
    found = {p.name for p in CSS_DIR.glob("style_*.css")}
    assert found == expected, (
        "Unexpected set of CSS files found.\n"
        f"Expected: {sorted(expected)}\n"
        f"Found   : {sorted(found)}"
    )


@pytest.mark.parametrize(
    "path,expected_content",
    [
        (STYLE_MAIN, EXPECTED_MAIN_CONTENT),
        (STYLE_THEME, EXPECTED_THEME_CONTENT),
    ],
)
def test_css_file_contents_are_exact(path: pathlib.Path, expected_content: str):
    """Verify that each CSS file's contents match the exercise specification."""
    content = path.read_text(encoding="utf-8")
    assert content == expected_content, (
        f"Contents of {path} do not match the expected specification."
    )