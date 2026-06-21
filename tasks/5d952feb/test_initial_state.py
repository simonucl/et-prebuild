# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state that must be
# present **before** the student starts writing their solution.  It checks
# only the input artefacts under /home/user/release_pages/ and deliberately
# ignores anything that will be created inside /home/user/deploy/.
#
# Requirements enforced here:
#   • /home/user/release_pages/ exists and is a directory.
#   • The three HTML files (alpha, beta, gamma) exist.
#   • Each file contains the expected first <h2> version tag and the
#     corresponding <p> release-date tag.
#
# When a check fails the assertion message explains exactly what is missing
# so that the learner can correct the environment before running their code.

import os
from pathlib import Path

import pytest

BASE_DIR = Path("/home/user/release_pages")

FILES_EXPECTATIONS = {
    "alpha_release.html": {
        "version": "<h2>v2.3.1</h2>",
        "date": "<p>Date: 2024-07-15</p>",
    },
    "beta_release.html": {
        "version": "<h2>v1.8.0</h2>",
        "date": "<p>Date: 2024-07-14</p>",
    },
    "gamma_release.html": {
        "version": "<h2>v5.0.0</h2>",
        "date": "<p>Date: 2024-07-10</p>",
    },
}


def test_release_pages_directory_exists():
    assert BASE_DIR.exists(), (
        f"Required directory {BASE_DIR} is missing. "
        "It must be present with the HTML release pages before the task starts."
    )
    assert BASE_DIR.is_dir(), (
        f"{BASE_DIR} exists but is not a directory. "
        "It must be a directory containing the release HTML files."
    )


@pytest.mark.parametrize("filename", FILES_EXPECTATIONS.keys())
def test_release_file_exists(filename):
    file_path = BASE_DIR / filename
    assert file_path.exists(), f"Expected file {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."


@pytest.mark.parametrize(
    "filename, expected_tags",
    [(fn, exp) for fn, exp in FILES_EXPECTATIONS.items()],
)
def test_release_file_content(filename, expected_tags):
    """
    Validate that each HTML release file contains the exact <h2> version tag
    and the matching <p> date tag as specified in the task description.
    """
    file_path = BASE_DIR / filename
    content = file_path.read_text(encoding="utf-8")

    version_tag = expected_tags["version"]
    date_tag = expected_tags["date"]

    assert version_tag in content, (
        f"{file_path} does not contain the expected version tag:\n"
        f"  expected: {version_tag}"
    )
    assert date_tag in content, (
        f"{file_path} does not contain the expected release-date tag:\n"
        f"  expected: {date_tag}"
    )

    # Optional sanity check: ensure the date tag appears *after* the version tag.
    assert content.index(version_tag) < content.index(date_tag), (
        f"In {file_path} the release date tag appears before the version tag. "
        "The <p> date line must immediately follow the <h2> version line."
    )

    # Verify the file ends with a newline to match the provided snippet.
    assert content.endswith("\n"), (
        f"{file_path} should end with a single newline (LF) character."
    )