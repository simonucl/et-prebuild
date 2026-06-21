# test_initial_state.py
#
# Pytest suite that validates the INITIAL state of the operating system /
# file-system before the student begins the assignment.
#
# It checks only the pre-existing material under /home/user/build_artifacts
# and deliberately ignores (does NOT look for) any of the output artefacts
# that the student is supposed to create later on.

from pathlib import Path
import pytest

# ---------------------------------------------------------------------------
# Constants describing the canonical initial state
# ---------------------------------------------------------------------------

ROOT_DIR = Path("/home/user/build_artifacts")
LIBS_DIR = ROOT_DIR / "libs"
CONFIGS_DIR = ROOT_DIR / "configs"

EXPECTED_FILES = {
    LIBS_DIR / "libalpha.txt": "Alpha library binary mock v1.0\n",
    LIBS_DIR / "libbeta.txt": "Beta library binary mock v1.0\n",
    CONFIGS_DIR / "app.conf": "[app]\nname=DemoApp\nversion=1.0.0\n",
    ROOT_DIR / "README.md": (
        "# Demo Build Artifacts\n"
        "These are mock artifacts for testing."  # NOTE: **no** trailing \n
    ),
}

EXPECTED_TOTAL_BYTES = 154  # Sum of the four files above


# ---------------------------------------------------------------------------
# Helper(s)
# ---------------------------------------------------------------------------

def _strict_read_text(path: Path) -> str:
    """
    Read text in strict mode (no universal-newline conversion) so that
    newline characters are accounted for exactly as stored on disk.
    """
    # open(..., newline='') gives the raw bytes decoding behaviour we want
    return path.open("r", encoding="utf-8", newline="").read()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist():
    """
    The build_artifacts tree and its two sub-directories must already exist.
    """
    for directory in (ROOT_DIR, LIBS_DIR, CONFIGS_DIR):
        assert directory.is_dir(), (
            f"Expected directory {directory} is missing "
            f"or is not recognised as a directory."
        )


@pytest.mark.parametrize("path,expected_content", EXPECTED_FILES.items())
def test_required_files_exist_with_exact_contents(path: Path, expected_content: str):
    """
    Every required file must be present and contain the exact, byte-for-byte
    string specified in the task description.
    """
    assert path.is_file(), f"Required file {path} is missing."
    actual_content = _strict_read_text(path)
    assert actual_content == expected_content, (
        f"Content mismatch in {path}.\n"
        f"Expected:\n{repr(expected_content)}\n"
        f"Found:\n{repr(actual_content)}"
    )


def test_dataset_size_matches_specification():
    """
    The sum of the byte sizes of the four required files must equal the
    canonical DATASET_SIZE_BYTES value given in the specification.
    """
    total_size = sum(path.stat().st_size for path in EXPECTED_FILES)
    assert total_size == EXPECTED_TOTAL_BYTES, (
        "DATASET_SIZE_BYTES mismatch.\n"
        f"Expected total: {EXPECTED_TOTAL_BYTES} bytes\n"
        f"Found total:    {total_size} bytes"
    )