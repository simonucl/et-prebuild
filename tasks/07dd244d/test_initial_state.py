# test_initial_state.py
#
# This pytest suite validates the operating-system / filesystem *before*
# the student performs any action.  It asserts that the expected “raw”
# Markdown drafts are present and *untouched*, and that none of the
# “processed” artefacts have been created yet.
#
# Only the Python stdlib + pytest are used.

from pathlib import Path
import pytest

HOME = Path("/home/user")
DOCS = HOME / "docs"
RAW_DIR = DOCS / "raw"
PROCESSED_DIR = DOCS / "processed"
LOG_FILE = DOCS / "processing.log"

# --------------------------------------------------------------------------- #
# Expected *initial* content of the raw Markdown drafts (byte-for-byte).
# Trailing spaces are significant and therefore explicitly included.
# --------------------------------------------------------------------------- #

EXPECTED_CONTENT = {
    "installation.md": (
        "# Installation\n"
        "To install the **AwesomeApp**, follow these steps:\n"
        "1. Download the package. [TODO] \n"
        "2. Run the installer.\n"
        "It will guide you through the setup.  \n"
    ).encode("utf-8"),

    "usage.md": (
        "# Usage Guide\n"
        "After installation, you can start AwesomeApp via terminal:\n"
        "$ awesomeapp start\n"
        "For advanced options, consult the manual. [TODO]  \n"
    ).encode("utf-8"),

    "changelog.md": (
        "# Changelog\n"
        "## v1.0.1\n"
        "- Fixed minor bugs.  \n"
        "## v1.0.0\n"
        "- Initial release. [TODO]\n"
    ).encode("utf-8"),
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #

def raw_path(name: str) -> Path:
    """Return the absolute path of `<name>` inside /home/user/docs/raw/."""
    return RAW_DIR / name


# --------------------------------------------------------------------------- #
# Tests for presence / absence of directories and files
# --------------------------------------------------------------------------- #

def test_raw_directory_exists():
    assert RAW_DIR.exists(), f"Directory {RAW_DIR} is missing."
    assert RAW_DIR.is_dir(), f"{RAW_DIR} exists but is not a directory."


def test_expected_raw_files_exist():
    missing = [name for name in EXPECTED_CONTENT if not raw_path(name).is_file()]
    assert not missing, (
        "The following expected Markdown drafts are missing in "
        f"{RAW_DIR}: {', '.join(missing)}"
    )


def test_processed_artifacts_do_not_exist_yet():
    assert not PROCESSED_DIR.exists(), (
        f"{PROCESSED_DIR} should NOT exist before the task is carried out."
    )
    assert not LOG_FILE.exists(), (
        f"{LOG_FILE} should NOT exist before the task is carried out."
    )


# --------------------------------------------------------------------------- #
# Tests that the raw Markdown files are *exactly* as described
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("filename", sorted(EXPECTED_CONTENT))
def test_raw_file_content_is_untouched(filename):
    """
    Verify that each raw Markdown file matches the byte-for-byte specification.
    Trailing whitespace and the final newline are both significant.
    """
    path = raw_path(filename)
    with path.open("rb") as fh:
        actual = fh.read()

    expected = EXPECTED_CONTENT[filename]

    # Helpful diff in assertion message if something changed.
    assert actual == expected, (
        f"Content mismatch in {path}.  "
        "The file must be exactly as provided at scenario start."
    )