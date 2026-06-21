# test_initial_state.py
#
# This test-suite validates the *initial* operating-system / filesystem
# state before the student begins the exercise.  It confirms that the
# original source tree is present and untouched while none of the
# artefacts that the task is supposed to create exist yet.

import hashlib
from pathlib import Path

import pytest

HOME = Path("/home/user")

# ---------- helpers -----------------------------------------------------------


def read_text(path: Path) -> str:
    """Return text content of *path* or fail with a useful message."""
    try:
        return path.read_text()
    except FileNotFoundError:  # pragma: no cover
        pytest.fail(f"Required file is missing: {path}")
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"Could not read {path}: {exc}")


def sha256sum(path: Path) -> str:
    """Return the hex SHA-256 of *path* (used to make sure we read the whole file)."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- expected values ---------------------------------------------------

RELEASE_ROOT = HOME / "releases" / "v2"
EXPECTED_FILES = {
    "README.md": """# App v2 Update
This release fixes bugs and improves performance.
""",
    "app.conf": """version=2.0.1
environment=production
debug=false
""",
    "scripts/start.sh": """#!/bin/bash
echo "Starting App v2..."
""",
}

DEPLOYMENTS_DIR = HOME / "deployments"
STAGING_DIR = DEPLOYMENTS_DIR / "staging"
TARBALL = DEPLOYMENTS_DIR / "app_update_v2.tar.gz"


# ---------- tests -------------------------------------------------------------


def test_release_tree_exists_and_correct():
    """
    Validate that /home/user/releases/v2 contains exactly the
    three expected files with the correct contents.
    """
    assert RELEASE_ROOT.is_dir(), f"Release directory missing: {RELEASE_ROOT}"

    # Collect every regular file relative to RELEASE_ROOT
    found_files = {
        str(path.relative_to(RELEASE_ROOT))
        for path in RELEASE_ROOT.rglob("*")
        if path.is_file()
    }

    expected_set = set(EXPECTED_FILES.keys())
    assert (
        found_files == expected_set
    ), f"Release tree should contain exactly {sorted(expected_set)}, found {sorted(found_files)}"

    # Validate contents are *exactly* as specified.
    for rel_path, expected_content in EXPECTED_FILES.items():
        file_path = RELEASE_ROOT / rel_path
        content = read_text(file_path)
        assert (
            content == expected_content
        ), f"Content mismatch in {file_path}.  Got:\n{content!r}\nExpected:\n{expected_content!r}"

        # Additional tiny sanity check: the file is non-empty and hashable
        assert sha256sum(file_path), f"Could not compute SHA-256 for {file_path}"


def test_no_deployment_artifacts_exist_yet():
    """
    Ensure that none of the artefacts produced by the forthcoming tasks
    are present prior to execution.
    """
    # The deployments directory may or may not exist yet.
    if DEPLOYMENTS_DIR.exists():
        assert not TARBALL.exists(), (
            f"Archive {TARBALL} should NOT exist before the user creates it."
        )
        assert (
            not STAGING_DIR.exists()
        ), f"Staging directory {STAGING_DIR} should NOT exist yet."
    else:
        # Directory itself absent is also acceptable (it will be created later).
        assert (
            True
        ), "Deployments directory does not exist yet, which is acceptable at this stage."