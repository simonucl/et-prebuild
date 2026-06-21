# test_initial_state.py
#
# Pytest suite that validates the *initial* state of the filesystem
# before the student carries out any actions.
#
# Do NOT modify the tests.  They are intended to guarantee that the
# operating-system state exactly matches the specification in the
# task description.

import re
from pathlib import Path
import pytest

BASE_DIR = Path("/home/user/stack")

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def _read_lines(path: Path):
    """
    Return a list of the file's lines without their trailing newlines.
    """
    return path.read_text(encoding="utf-8").splitlines()


# --------------------------------------------------------------------------- #
# Expected data taken from the task description
# --------------------------------------------------------------------------- #
EXPECTED_FILES = {
    "compose-auth.yml": [
        "services:",
        "  auth-db:",
        "    image: postgres:13",
        "  auth-service:",
        "    image: myregistry/auth-service:1.2.0",
    ],
    "compose-data.yml": [
        "services:",
        "  redis:",
        "    image: redis:6-alpine",
        "  data-service:",
        "    image: myregistry/data-service:3.4.5",
        "  auth-db:",
        "    image: postgres:13",
    ],
    "compose-api.yml": [
        "services:",
        "  api-gateway:",
        "    image: myregistry/api-gateway:2.0.0",
        "  auth-service:",
        "    image: myregistry/auth-service:1.2.0",
    ],
}

# All images that must be present across the *.yml files
EXPECTED_IMAGES = {
    "postgres:13",
    "myregistry/auth-service:1.2.0",
    "redis:6-alpine",
    "myregistry/data-service:3.4.5",
    "myregistry/api-gateway:2.0.0",
}


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_base_directory_exists():
    assert BASE_DIR.is_dir(), (
        f"Expected directory {BASE_DIR} to exist, "
        "but it is missing or not a directory."
    )


def test_expected_compose_files_present_and_no_extras():
    """
    Verify that the directory contains *exactly* the three expected *.yml files
    and nothing more with a `.yml` suffix.
    """
    found_files = sorted(p.name for p in BASE_DIR.glob("*.yml"))
    expected_files = sorted(EXPECTED_FILES.keys())

    assert (
        found_files == expected_files
    ), (
        "The set of *.yml files in /home/user/stack/ does not match "
        "the specification.\n"
        f"Expected files: {expected_files}\n"
        f"Found files   : {found_files}"
    )


@pytest.mark.parametrize("filename,expected_lines", EXPECTED_FILES.items())
def test_exact_file_contents(filename, expected_lines):
    """
    Validate that each compose file's contents match the specification line-by-line.
    Trailing newlines are tolerated; only significant text is compared.
    """
    path = BASE_DIR / filename
    assert path.is_file(), f"Expected file {path} to exist."

    actual_lines = _read_lines(path)
    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {path} do not match the expected initial state.\n"
        "---- Expected (line-by-line) ----\n"
        + "\n".join(expected_lines)
        + "\n---- Actual ----\n"
        + "\n".join(actual_lines)
    )


def test_images_referenced_are_exactly_the_expected_set():
    """
    Parse all compose files for `image:` keys and ensure the set of images
    exactly matches the specification (order and duplicates are irrelevant here).
    """
    image_regex = re.compile(r"^\s*image:\s*(.+)$")
    found_images = set()

    for path in BASE_DIR.glob("*.yml"):
        for line in _read_lines(path):
            m = image_regex.match(line)
            if m:
                found_images.add(m.group(1).strip())

    assert (
        found_images == EXPECTED_IMAGES
    ), (
        "The set of container images referenced in the compose files "
        "does not match the expected initial state.\n"
        f"Expected images: {sorted(EXPECTED_IMAGES)}\n"
        f"Found images   : {sorted(found_images)}"
    )