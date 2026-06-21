# test_initial_state.py
#
# Pytest suite to validate the initial filesystem state **before** the student
# performs any actions.  These tests must pass out-of-the-box; if they fail
# it means the exercise environment is not correctly provisioned.
#
# IMPORTANT:
#   • We deliberately do NOT test for any output files or directories that
#     the student is supposed to create (/home/user/backups/…, /home/user/backup_logs/…).
#   • We only assert the presence and exact content of the pre-existing
#     experiment files under /home/user/experiments.

import hashlib
from pathlib import Path

import pytest


HOME = Path("/home/user")
EXP_ROOT = HOME / "experiments"

# Expected relative file paths (relative to /home/user) and their exact content.
EXPECTED_FILES = {
    "experiments/run_001/model.pkl": "run_001 model checkpoint\n",
    "experiments/run_001/metrics.json": '{"accuracy": 0.91, "loss": 0.23}\n',
    "experiments/run_002/model.pkl": "run_002 model checkpoint\n",
    "experiments/run_002/metrics.json": '{"accuracy": 0.93, "loss": 0.19}\n',
}


def _collect_all_regular_files(root: Path):
    """Return a set of all regular files under 'root', expressed as
    POSIX-style paths *relative to /home/user* (so every path string starts
    with 'experiments/…'). Symlinks, dirs, etc. are ignored."""
    all_files = set()
    for path in root.rglob("*"):
        if path.is_file():
            rel = path.relative_to(HOME).as_posix()
            all_files.add(rel)
    return all_files


def _file_md5(path: Path) -> str:
    """Return lowercase MD5 hex digest of the file at *path*."""
    hasher = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


@pytest.mark.dependency(name="dir_exists")
def test_experiments_directory_exists_and_is_directory():
    assert EXP_ROOT.exists(), f"Expected directory {EXP_ROOT} is missing."
    assert EXP_ROOT.is_dir(), f"{EXP_ROOT} exists but is not a directory."


@pytest.mark.dependency(depends=["dir_exists"], name="file_set")
def test_expected_file_set_is_complete_and_exclusive():
    """Ensure the experiments tree contains exactly the expected files."""
    found = _collect_all_regular_files(EXP_ROOT)
    expected = set(EXPECTED_FILES)
    missing = expected - found
    extra = found - expected

    assert not missing, (
        "The following expected files are missing:\n  - "
        + "\n  - ".join(sorted(missing))
    )
    assert not extra, (
        "Unexpected extra files present in /home/user/experiments:\n  - "
        + "\n  - ".join(sorted(extra))
    )


@pytest.mark.dependency(depends=["file_set"])
@pytest.mark.parametrize("rel_path,expected_content", sorted(EXPECTED_FILES.items()))
def test_file_contents(rel_path, expected_content):
    """Verify each file's byte-for-byte contents are exactly as expected."""
    abs_path = HOME / rel_path
    assert abs_path.exists(), f"File {abs_path} is missing."

    # Read as binary to ensure byte-level fidelity, then decode as UTF-8.
    raw = abs_path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"File {abs_path} is not valid UTF-8: {exc}")

    assert (
        text == expected_content
    ), f"Contents of {abs_path} do not match the expected fixture."

    # As an additional safeguard, check MD5 of each file matches the EXPECTED_CONTENT
    # instance to rule out hidden differences (e.g., CRLF vs LF).
    expected_md5 = hashlib.md5(expected_content.encode()).hexdigest()
    actual_md5 = _file_md5(abs_path)
    assert (
        actual_md5 == expected_md5
    ), f"MD5 checksum mismatch for {abs_path}: expected {expected_md5}, got {actual_md5}"