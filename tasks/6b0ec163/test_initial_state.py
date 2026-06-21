# test_initial_state.py
#
# This pytest suite validates the *initial* on–disk state of
# the micro-benchmark project located at /home/user/perf_project.
#
# IMPORTANT:  These checks run **before** the student makes any
# modifications, therefore they must not look for the final
# artefact (security_scan.log) or any other files that are yet
# to be created.

import os
import re
from pathlib import Path

PROJECT_ROOT = Path("/home/user/perf_project").resolve()

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_text(path: Path) -> str:
    """Return file contents as text.  Fails with a helpful message if unreadable."""
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:  # pragma: no cover
        raise AssertionError(f"Required file missing: {path}")
    except OSError as exc:  # pragma: no cover
        raise AssertionError(f"Could not read {path}: {exc}") from exc


def count_token_occurrences(text: str, token: str) -> int:
    """
    Return the number of occurrences of a C function call token such as 'strcpy('
    using a word boundary to avoid partial matches.
    """
    pattern = rf"\b{re.escape(token)}\s*\("
    return len(re.findall(pattern, text))


# ---------------------------------------------------------------------------
# Tests for directory structure
# ---------------------------------------------------------------------------

def test_project_root_exists_and_is_directory():
    assert PROJECT_ROOT.exists(), f"Expected project directory at {PROJECT_ROOT} but it does not exist."
    assert PROJECT_ROOT.is_dir(), f"Path {PROJECT_ROOT} exists but is not a directory."


# List of source files that **must** be present.
REQUIRED_FILES = {
    "main.c",
    "util.c",
    "util.h",
}


def test_required_source_files_exist_and_are_regular_files():
    missing = []
    not_regular = []
    for fname in REQUIRED_FILES:
        fpath = PROJECT_ROOT / fname
        if not fpath.exists():
            missing.append(str(fpath))
        elif not fpath.is_file():
            not_regular.append(str(fpath))

    assert not missing, f"The following required files are missing: {', '.join(missing)}"
    assert not not_regular, f"The following paths exist but are not regular files: {', '.join(not_regular)}"


# ---------------------------------------------------------------------------
# Tests for insecure function occurrences
# ---------------------------------------------------------------------------

EXPECTED_CALLS = {
    # file_name  -> {token: expected_minimum_occurrences}
    "main.c": {"strcpy": 2, "sprintf": 1},
    "util.c": {"gets": 1},
}


def _verify_token_counts(src_path: Path, token: str, expected_min: int):
    """Helper that asserts the given token occurs at least expected_min times in the file."""
    text = read_text(src_path)
    actual = count_token_occurrences(text, token)
    assert actual >= expected_min, (
        f"Insecure function '{token}' expected >= {expected_min} occurrences in {src_path}, "
        f"found {actual}."
    )


def test_insecure_function_calls_present():
    """
    Validate that each insecure C-library function appears the expected number
    of times in the corresponding source files.
    """
    for file_name, token_map in EXPECTED_CALLS.items():
        src_path = PROJECT_ROOT / file_name
        assert src_path.exists(), f"Required source file missing: {src_path}"
        for token, expected_min in token_map.items():
            _verify_token_counts(src_path, token, expected_min)