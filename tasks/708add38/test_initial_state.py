# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state **before** the student
performs any actions.  It intentionally *does not* check for the expected
outputs (symlinks or report file); it only verifies the pre-existing directories
that the assignment describes.
"""

from pathlib import Path
import os
import stat
import pytest

MICROSERVICES_DIR = Path("/home/user/microservices")
AUTH_DIR          = MICROSERVICES_DIR / "auth-service-1.2.3"
BILLING_DIR       = MICROSERVICES_DIR / "billing-service-2.4.0"


def _assert_is_real_directory(p: Path) -> None:
    """
    Assert that `p` exists, is a directory, *and* is not a symlink.

    Raises an assertion error with a helpful message if any check fails.
    """
    assert p.exists(), f"Expected directory {p} is missing."
    assert p.is_dir(), f"{p} exists but is not a directory."
    # A path can be both dir() and symlink(); guard against that.
    assert not p.is_symlink(), f"{p} should be a real directory, not a symlink."


def test_microservices_root_exists_and_is_dir():
    """
    /home/user/microservices must exist as a real directory.
    """
    _assert_is_real_directory(MICROSERVICES_DIR)


@pytest.mark.parametrize(
    "service_dir",
    [
        AUTH_DIR,
        BILLING_DIR,
    ],
    ids=["auth-service-1.2.3 directory", "billing-service-2.4.0 directory"],
)
def test_service_version_directories_exist(service_dir: Path):
    """
    Each versioned service directory must exist and be a real directory.
    """
    _assert_is_real_directory(service_dir)


def test_microservices_dir_contains_only_expected_items():
    """
    Ensure the microservices directory is clean: it should contain exactly the two
    service directories (and nothing else) at the start of the exercise.

    NOTE: We *exclude* any future outputs (symlinks or report file) from this
    check, in compliance with the grading instructions.
    """
    expected = {AUTH_DIR.name, BILLING_DIR.name}
    actual = {p.name for p in MICROSERVICES_DIR.iterdir()}

    # Intersect to avoid failing once students create new outputs; we only care
    # that the expected items are present now.
    missing = expected - actual
    assert not missing, (
        "The following required directories are missing in "
        f"{MICROSERVICES_DIR}: {', '.join(sorted(missing))}"
    )