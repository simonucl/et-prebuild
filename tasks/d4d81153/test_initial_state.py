# test_initial_state.py
#
# This pytest suite validates that the container’s filesystem is in the
# *pristine* state that students are expected to start from – before they carry
# out any of the task steps.
#
# It deliberately fails fast with clear, actionable error messages whenever a
# required file, directory or piece of content is missing or differs from what
# the exercise specification promises.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
RELEASES_DIR = HOME / "releases"

# Expected release payloads and the exact README contents for each one
EXPECTED_PAYLOADS = {
    "auth-service-3.4.1": "Auth service build 3.4.1\n",
    "data-service-2.1.0": "Data service build 2.1.0\n",
    "gateway-service-1.8.7": "Gateway service build 1.8.7\n",
}

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def assert_dir(path: Path):
    """Assert that *path* exists and is a directory."""
    assert path.exists(), f"Expected directory {path!s} to exist."
    assert path.is_dir(), f"{path!s} exists but is not a directory."


def assert_file_with_content(path: Path, expected_content: str):
    """Assert that *path* exists, is file, and contains *expected_content*."""
    assert path.exists(), f"Expected file {path!s} to exist."
    assert path.is_file(), f"{path!s} exists but is not a regular file."
    actual = path.read_text(encoding="utf-8")
    assert (
        actual == expected_content
    ), f"File {path!s} has unexpected contents:\n{actual!r}\nExpected:\n{expected_content!r}"


# --------------------------------------------------------------------------- #
# Tests that describe the **initial** state of the container’s filesystem
# --------------------------------------------------------------------------- #
def test_releases_directory_exists():
    """/home/user/releases must be a directory."""
    assert_dir(RELEASES_DIR)


@pytest.mark.parametrize("payload_dir, readme_content", EXPECTED_PAYLOADS.items())
def test_each_payload_present_with_correct_readme(payload_dir, readme_content):
    """
    Every expected micro-service release directory must exist and include a
    README.md containing the exact text promised by the task description.
    """
    payload_path = RELEASES_DIR / payload_dir
    readme_path = payload_path / "README.md"

    assert_dir(payload_path)
    assert_file_with_content(readme_path, readme_content)


def test_no_extra_gateway_1_9_0_release_yet():
    """
    The new gateway-service-1.9.0 directory must NOT exist at the beginning.
    It is something the student is supposed to create.
    """
    forbidden = RELEASES_DIR / "gateway-service-1.9.0"
    assert not forbidden.exists(), (
        f"Directory {forbidden!s} is present, but it should not exist in the "
        "initial state."
    )


def test_current_release_directory_absent():
    """
    /home/user/current-release must NOT exist yet (neither directory nor link).
    The student will create it.
    """
    current_release = HOME / "current-release"
    assert not current_release.exists(), (
        f"{current_release!s} already exists – it must be created by the student."
    )


def test_link_report_absent():
    """
    /home/user/link-report.txt must not exist yet; the student will generate it.
    """
    link_report = HOME / "link-report.txt"
    assert not link_report.exists(), (
        f"{link_report!s} already exists – it must be produced by the student."
    )