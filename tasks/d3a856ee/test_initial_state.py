# test_initial_state.py
#
# This pytest suite validates the filesystem **before** the student
# performs any actions.  It confirms that the two configuration files
# are present with their expected *initial* contents and that the
# directory where the future log file will live already exists.
#
# NOTE:  We purposely do **not** check for the presence or absence
#        of the log file the student will create, because the grader
#        rules forbid testing for output artefacts.

import os
from pathlib import Path

# ---------------------------------------------------------------------------
# Constant paths
# ---------------------------------------------------------------------------

HOME = Path("/home/user")
CFG_DIR = HOME / "server_configs"
CHANGELOG_DIR = HOME / "change_logs"

APP_YAML = CFG_DIR / "app.yaml"
DB_TOML = CFG_DIR / "db.toml"


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_file(path: Path) -> list[str]:
    """Read *all* lines from a text file, preserving newlines."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.readlines()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_app_yaml_exists_with_expected_initial_values():
    assert APP_YAML.is_file(), (
        f"Expected the YAML config file to exist at {APP_YAML}, "
        "but it is missing."
    )

    lines = read_file(APP_YAML)

    # The file should at minimum include the following five exact lines
    expected_lines = [
        "server:\n",
        "  host: 0.0.0.0\n",
        "  port: 8080\n",
        "  debug: true\n",
        "  maintenance: false\n",
    ]

    # Quick sanity-check: number of lines
    assert len(lines) == len(expected_lines), (
        f"{APP_YAML} should contain {len(expected_lines)} lines, "
        f"but has {len(lines)}."
    )

    # Exact line-by-line comparison
    for idx, (actual, expected) in enumerate(zip(lines, expected_lines), start=1):
        assert actual == expected, (
            f"Line {idx} of {APP_YAML} differs from expected.\n"
            f"  Expected: {expected!r}\n"
            f"  Found   : {actual!r}"
        )


def test_db_toml_exists_with_expected_initial_values():
    assert DB_TOML.is_file(), (
        f"Expected the TOML config file to exist at {DB_TOML}, "
        "but it is missing."
    )

    lines = read_file(DB_TOML)

    # Expected content (eight lines including section header and trailing newline)
    expected_lines = [
        "[database]\n",
        'user = "admin"\n',
        'password = "oldpass"\n',
        'host = "localhost"\n',
        "port = 5432\n",
        "max_connections = 100\n",
    ]

    # The file is expected to have exactly len(expected_lines) lines.
    # Some editors automatically append a blank line at the end; tolerate that
    # as long as content lines are correct and in order.
    content_lines = lines[: len(expected_lines)]
    trailing_lines = lines[len(expected_lines):]

    assert content_lines == expected_lines, (
        f"The contents of {DB_TOML} are not as expected.\n"
        "If you see this failure, ensure the initial file has not been "
        "modified before the test runs."
    )

    # Any extra lines must be blank (i.e., only '\n')
    for extra in trailing_lines:
        assert extra.strip() == "", (
            f"Unexpected non-blank extra line found in {DB_TOML!s}: {extra!r}"
        )


def test_changelog_directory_exists_and_is_directory():
    assert CHANGELOG_DIR.exists(), (
        f"Expected directory {CHANGELOG_DIR} to exist, but it is missing."
    )
    assert CHANGELOG_DIR.is_dir(), (
        f"Expected {CHANGELOG_DIR} to be a directory, but it is not."
    )
    # Additionally, ensure we have write permission
    assert os.access(CHANGELOG_DIR, os.W_OK), (
        f"Directory {CHANGELOG_DIR} is not writable by the current user."
    )