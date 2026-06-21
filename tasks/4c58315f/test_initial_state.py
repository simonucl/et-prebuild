# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student begins working on the task.  It purposefully
# checks ONLY the pre-existing files and directories and does **not**
# look for (or complain about) any of the target artefacts that the
# student is asked to create later.

import pathlib

DOCS_DIR = pathlib.Path("/home/user/docs")


def test_docs_root_exists():
    """Verify that /home/user/docs exists and is a directory."""
    assert DOCS_DIR.is_dir(), (
        "The directory /home/user/docs does not exist or is not a directory."
    )


def test_subdirectories_exist():
    """Ensure the expected sub-directories are present."""
    articles = DOCS_DIR / "articles"
    tutorials = DOCS_DIR / "tutorials"

    assert articles.is_dir(), "Missing directory: /home/user/docs/articles"
    assert tutorials.is_dir(), "Missing directory: /home/user/docs/tutorials"


def test_article_markdown_files_exist():
    """Check that both article markdown files exist."""
    intro = DOCS_DIR / "articles" / "intro.md"
    setup = DOCS_DIR / "articles" / "setup.md"

    assert intro.is_file(), "Missing file: /home/user/docs/articles/intro.md"
    assert setup.is_file(), "Missing file: /home/user/docs/articles/setup.md"


def test_tutorial_markdown_file_exists():
    """Check that the tutorial markdown file exists."""
    overview = DOCS_DIR / "tutorials" / "overview.md"
    assert overview.is_file(), "Missing file: /home/user/docs/tutorials/overview.md"


def _first_line(path):
    """Return the first line of a text file, stripped of newline characters."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readline().rstrip("\n")


def test_markdown_first_lines():
    """Validate the first line (title) of each markdown file."""
    expected_titles = {
        DOCS_DIR / "articles" / "intro.md": "# Introduction",
        DOCS_DIR / "articles" / "setup.md": "# Setup",
        DOCS_DIR / "tutorials" / "overview.md": "# Overview",
    }

    for file_path, expected in expected_titles.items():
        assert file_path.is_file(), f"Missing file: {file_path}"
        got = _first_line(file_path)
        assert (
            got == expected
        ), f"First line of {file_path} is '{got}', expected '{expected}'."


def test_site_config_exists():
    """Ensure that the pre-existing TOML configuration file is present."""
    cfg = DOCS_DIR / "site_config.toml"
    assert cfg.is_file(), "Missing file: /home/user/docs/site_config.toml"