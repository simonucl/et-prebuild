# test_initial_state.py
#
# Pytest suite that validates the expected *initial* state of the localisation
# project before the student performs any actions.
#
# It checks:
#   • Presence of the /home/user/project/locales directory.
#   • Presence of the three required seed files.
#   • Exact byte-for-byte contents (including line endings and trailing LF)
#     of those seed files.
#
# NOTE:  We intentionally do *not* test for the presence or absence of any
#        output artefacts (e.g. translations_update.log) in accordance with
#        the grading rules.

import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/project/locales")

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def assert_unix_newline_at_eof(content: bytes, file_path: Path) -> None:
    """
    Assert that:
      1. The file ends with exactly one LF ('\n').
      2. The file contains no CR ('\r') characters.
    """
    assert b"\r" not in content, (
        f"{file_path} must use UNIX line endings (LF) only; found CR characters."
    )
    assert content.endswith(b"\n"), (
        f"{file_path} must terminate with a single UNIX line-feed (LF)."
    )
    # Ensure *exactly* one trailing newline
    assert not content.endswith(b"\n\n"), (
        f"{file_path} must end with exactly one trailing newline, "
        "not multiple consecutive newlines."
    )


def read_file_bytes(path: Path) -> bytes:
    """Read a file in binary mode and return its raw bytes."""
    with path.open("rb") as fh:
        return fh.read()


# --------------------------------------------------------------------------- #
# Expected reference contents (byte-exact, including final LF)
# --------------------------------------------------------------------------- #
EXPECTED_EN_US = (
    "KEY,VALUE\n"
    "greeting,Hello\n"
    "farewell,Goodbye\n"
    "ask_name,What is your name?\n"
    "confirm,Are you sure?\n"
).encode("utf-8")

EXPECTED_FR_FR_INITIAL = (
    "KEY,VALUE\n"
    "greeting,Bonjour\n"
    "farewell,\n"
    "ask_name,\n"
    "confirm,Etes-vous sûr?\n"
).encode("utf-8")

EXPECTED_TO_ADD_FR = (
    "farewell=Au revoir\n"
    "ask_name=Comment vous appelez-vous?\n"
).encode("utf-8")


# Mapping: relative file path → expected content bytes
SEED_FILES_EXPECTED = {
    Path("en_US.csv"): EXPECTED_EN_US,
    Path("fr_FR.csv"): EXPECTED_FR_FR_INITIAL,
    Path("to_add_fr.txt"): EXPECTED_TO_ADD_FR,
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_locales_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Required directory '{BASE_DIR}' does not exist."
    )


@pytest.mark.parametrize("relative_path, expected_bytes", SEED_FILES_EXPECTED.items())
def test_seed_file_content(relative_path: Path, expected_bytes: bytes):
    full_path = BASE_DIR / relative_path
    assert full_path.is_file(), (
        f"Required file '{full_path}' is missing."
    )

    content = read_file_bytes(full_path)

    assert_unix_newline_at_eof(content, full_path)

    assert content == expected_bytes, (
        f"Contents of '{full_path}' do not match the expected initial state.\n"
        f"--- Expected ---\n{expected_bytes.decode('utf-8')!r}\n"
        f"--- Found ---\n{content.decode('utf-8')!r}"
    )