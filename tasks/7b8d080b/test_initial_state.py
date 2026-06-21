# test_initial_state.py
#
# Pytest suite that validates the initial filesystem layout for the
# distributed-training manifest exercise.  It checks that the expected
# directory tree exists under /home/user/distr_exp/run_42 and that the
# four artefact files are present, regular, empty, and nothing else is
# in those node directories.  No assertions are made about the final
# output file (manifest.sha1) because that is produced *after* the
# student’s command is run.

import hashlib
from pathlib import Path

import pytest

ROOT = Path("/home/user/distr_exp/run_42")
NODE_DIRS = [ROOT / "node01", ROOT / "node02"]
EXPECTED_FILES = [
    NODE_DIRS[0] / "model.bin",
    NODE_DIRS[0] / "metrics.json",
    NODE_DIRS[1] / "model.bin",
    NODE_DIRS[1] / "metrics.json",
]
EMPTY_SHA1 = "da39a3ee5e6b4b0d3255bfef95601890afd80709"


def sha1_of_file(path: Path) -> str:
    """Return lower-case hex SHA-1 of the file at *path*."""
    h = hashlib.sha1()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def test_root_directory_exists():
    assert ROOT.exists(), (
        f"Required root directory {ROOT} does not exist. "
        "The exercise expects the training artefacts to live here."
    )
    assert ROOT.is_dir(), f"{ROOT} exists but is not a directory."


@pytest.mark.parametrize("node_dir", NODE_DIRS)
def test_node_directories_exist(node_dir: Path):
    assert node_dir.exists(), f"Expected node directory {node_dir} is missing."
    assert node_dir.is_dir(), f"{node_dir} exists but is not a directory."


@pytest.mark.parametrize("file_path", EXPECTED_FILES)
def test_expected_files_present_and_empty(file_path: Path):
    assert file_path.exists(), f"Expected artefact {file_path} is missing."
    assert file_path.is_file(), f"{file_path} exists but is not a regular file."

    # Size check
    size = file_path.stat().st_size
    assert size == 0, (
        f"{file_path} is expected to be empty, but its size is {size} bytes."
    )

    # Content (SHA-1 of empty content)
    actual_hash = sha1_of_file(file_path)
    assert (
        actual_hash == EMPTY_SHA1
    ), f"{file_path} should have SHA-1 {EMPTY_SHA1}, got {actual_hash}."


@pytest.mark.parametrize("node_dir, expected_files", [
    (NODE_DIRS[0], {EXPECTED_FILES[0].name, EXPECTED_FILES[1].name}),
    (NODE_DIRS[1], {EXPECTED_FILES[2].name, EXPECTED_FILES[3].name}),
])
def test_no_extra_files_in_node_dirs(node_dir: Path, expected_files: set):
    present_files = {p.name for p in node_dir.iterdir() if p.is_file()}
    assert present_files == expected_files, (
        f"{node_dir} contains unexpected files.\n"
        f"Expected exactly: {sorted(expected_files)}\n"
        f"Found: {sorted(present_files)}"
    )