# test_initial_state.py
#
# Pytest suite that verifies the *initial* filesystem state for the
# “artifact-manager” exercise.  These tests must all PASS **before**
# the student starts working on the task.  Any failure means the
# playground is not in the expected pristine state.

import hashlib
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
ARTIFACTS = HOME / "artifacts"
SOURCE = ARTIFACTS / "source"
RELEASES = ARTIFACTS / "releases"
STAGING = ARTIFACTS / "staging"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------------------
# Tests for the directory structure
# ---------------------------------------------------------------------------


def test_required_directories_exist_and_are_dirs():
    """
    Verify that the four required directories exist and are directories.
    """
    for p in (ARTIFACTS, SOURCE, RELEASES, STAGING):
        assert p.exists(), f"Required directory {p} is missing."
        assert p.is_dir(), f"{p} exists but is not a directory."


def test_root_contains_only_expected_directories():
    """
    /home/user/artifacts/ must contain exactly the three directories
    'source', 'releases', and 'staging' – no files and no extra dirs.
    """
    entries = {e.name for e in ARTIFACTS.iterdir()}
    expected = {"source", "releases", "staging"}
    assert entries == expected, (
        "Unexpected content in /home/user/artifacts/.\n"
        f"Expected: {sorted(expected)}\n"
        f"Found   : {sorted(entries)}"
    )


# ---------------------------------------------------------------------------
# Tests for files inside /source
# ---------------------------------------------------------------------------

EXPECTED_SOURCE_FILES = {
    "binary1.bin": {
        "size": 250,
        "content": (b"BIN1\n" * 50),
    },
    "binary2.bin": {
        "size": 250,
        "content": (b"BIN2\n" * 50),
    },
    "readme.txt": {
        "size": 48,
        "content": b"These are sample binaries for compression test.\n",
    },
}


@pytest.mark.parametrize("filename", EXPECTED_SOURCE_FILES.keys())
def test_source_file_presence_and_size(filename):
    """
    Each expected file must exist and have the correct byte size.
    """
    path = SOURCE / filename
    assert path.exists(), f"Missing file {path}"
    assert path.is_file(), f"{path} exists but is not a regular file"
    expected_size = EXPECTED_SOURCE_FILES[filename]["size"]
    actual_size = path.stat().st_size
    assert (
        actual_size == expected_size
    ), f"{path} size mismatch: expected {expected_size} bytes, got {actual_size}."


@pytest.mark.parametrize("filename", EXPECTED_SOURCE_FILES.keys())
def test_source_file_content_exact_match(filename):
    """
    File contents must match exactly the prescribed bytes.
    """
    path = SOURCE / filename
    with path.open("rb") as f:
        data = f.read()
    expected_content = EXPECTED_SOURCE_FILES[filename]["content"]
    assert (
        data == expected_content
    ), f"Content of {path} does not match the expected initial content."


def test_no_extra_files_in_source():
    """
    Ensure that /source contains ONLY the three expected files.
    """
    entries = {e.name for e in SOURCE.iterdir()}
    expected = set(EXPECTED_SOURCE_FILES.keys())
    assert entries == expected, (
        "Unexpected content in /home/user/artifacts/source/.\n"
        f"Expected files: {sorted(expected)}\n"
        f"Found         : {sorted(entries)}"
    )


# ---------------------------------------------------------------------------
# Tests for emptiness of /releases and /staging
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("directory", [RELEASES, STAGING])
def test_releases_and_staging_are_empty(directory: Path):
    """
    The releases/ and staging/ directories must be completely empty at the start.
    """
    contents = list(directory.iterdir())
    assert (
        len(contents) == 0
    ), f"{directory} is expected to be empty, but contains: {[c.name for c in contents]}"


# ---------------------------------------------------------------------------
# Tests ensuring *absence* of files that should not yet exist
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "unexpected_path",
    [
        RELEASES / "binaries_backup.tar.gz",
        RELEASES / "docs.zip",
        ARTIFACTS / "release_log.txt",
    ],
)
def test_output_artifacts_do_not_exist_yet(unexpected_path: Path):
    """
    Output artifacts must NOT exist in the initial state.
    """
    assert (
        not unexpected_path.exists()
    ), f"File {unexpected_path} should not exist before the student starts the task."


# ---------------------------------------------------------------------------
# Sanity check: no hidden surprises in the entire tree
# ---------------------------------------------------------------------------


def test_no_hidden_surprises_in_artifacts_tree():
    """
    Traverse the artifacts/ tree and ensure that only the allowed paths
    exist.  This is a stricter catch-all to detect files or dirs that
    slipped through the cracks.
    """
    allowed = {
        ARTIFACTS,
        SOURCE,
        RELEASES,
        STAGING,
        *(SOURCE / name for name in EXPECTED_SOURCE_FILES),
    }
    found = set()

    for root, dirs, files in os.walk(ARTIFACTS):
        for d in dirs:
            found.add(Path(root) / d)
        for f in files:
            found.add(Path(root) / f)
        found.add(Path(root))  # include the directory itself

    unexpected = {p for p in found if p not in allowed}
    assert not unexpected, (
        "Unexpected files or directories present in the initial state:\n"
        + "\n".join(str(p) for p in sorted(unexpected))
    )