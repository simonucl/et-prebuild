# test_initial_state.py
#
# This pytest file validates the PRE-TASK state of the filesystem.
# It ensures that only the seed material provided by the platform is
# present and correct.  Any failures here signal that the workspace is
# already in an unexpected state *before* the student begins the task.
#
# IMPORTANT:  These tests *deliberately* avoid looking for any files or
# directories that the student is supposed to create (e.g. the encrypted
# artefacts or log files).  They verify only what must already exist.

from pathlib import Path
import pytest

# Base directory used throughout the assignment
BASE_DIR = Path("/home/user/compliance_work")

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def read_first_n_lines(path: Path, n: int = 1) -> list[str]:
    """
    Return the first `n` lines of the file located at `path`.
    The file is read in text mode with UTF-8 encoding and universal newlines.
    """
    with path.open("r", encoding="utf-8", newline=None) as fh:
        return [next(fh).rstrip("\n") for _ in range(n)]


# ---------------------------------------------------------------------------
# Tests for the pre-existing seed material
# ---------------------------------------------------------------------------

def test_base_directory_exists_and_is_directory():
    """
    The main working directory `/home/user/compliance_work` must already exist.
    """
    assert BASE_DIR.exists(), (
        f"Expected directory {BASE_DIR} is missing. "
        "The initial workspace is not set up correctly."
    )
    assert BASE_DIR.is_dir(), (
        f"{BASE_DIR} exists but is not a directory. "
        "A directory is required as the base workspace."
    )


@pytest.mark.parametrize(
    "relative_path, expected_first_line",
    [
        ("client_data.csv", "id,name,balance"),
        ("code_of_conduct.txt", "ACME CORPORATION – CODE OF CONDUCT"),
    ],
)
def test_seed_files_exist_with_correct_first_line(relative_path, expected_first_line):
    """
    Verify that each required seed file exists and that its first line
    matches the canonical content shipped with the exercise.
    """
    file_path = BASE_DIR / relative_path

    assert file_path.exists(), (
        f"Required seed file {file_path} is missing. "
        "The workspace is corrupt."
    )
    assert file_path.is_file(), (
        f"{file_path} exists but is not a regular file. "
        "Expected a plain text file."
    )

    # Ensure the file has at least one line and that the first line matches.
    try:
        first_line = read_first_n_lines(file_path, 1)[0]
    except (StopIteration, IndexError):
        pytest.fail(f"{file_path} is empty. "
                    "Seed files must contain the expected content.")

    assert first_line == expected_first_line, (
        f"The first line of {file_path} does not match the expected content.\n"
        f"Expected: {expected_first_line!r}\n"
        f"Found   : {first_line!r}"
    )


def test_detached_signature_file_exists_and_is_non_empty():
    """
    The detached signature accompanying the code of conduct must already
    be present.  It is expected to be a plain text file whose *size* is
    non-zero (content validation happens later during the student's work).
    """
    sig_path = BASE_DIR / "code_of_conduct.txt.sig"

    assert sig_path.exists(), (
        f"Detached signature file {sig_path} is missing."
    )
    assert sig_path.is_file(), (
        f"{sig_path} exists but is not a regular file."
    )
    assert sig_path.stat().st_size > 0, (
        f"{sig_path} is empty. A non-empty signature file is required."
    )