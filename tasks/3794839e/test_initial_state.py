# test_initial_state.py
#
# This test-suite validates that the filesystem is in the expected *initial*
# state before the student begins the task.
#
# It asserts:
#   • Required directories under /home/user/mlops/ exist.
#   • Three experiment sub-directories exist (alpha, beta, gamma).
#   • Each experiment contains an artifacts.txt file whose byte-for-byte
#     content exactly matches the specification (including terminating
#     newlines).
#   • The summary directory /home/user/mlops/summary/ ‑-and therefore
#     /home/user/mlops/summary/artifacts_summary.txt-- do **not** exist yet.
#
# If any assertion fails, the error message will precisely describe what is
# missing or out of place.
#
# The tests rely only on the standard library and pytest.

import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
MLOPS_DIR = HOME / "mlops"
EXPERIMENTS_DIR = MLOPS_DIR / "experiments"
SUMMARY_DIR = MLOPS_DIR / "summary"           # must NOT exist initially
SUMMARY_FILE = SUMMARY_DIR / "artifacts_summary.txt"

# -----------------------------------------------------------------------------
# Expected directory structure
# -----------------------------------------------------------------------------
EXPECTED_DIRS = [
    HOME,
    MLOPS_DIR,
    EXPERIMENTS_DIR,
    EXPERIMENTS_DIR / "exp_alpha",
    EXPERIMENTS_DIR / "exp_beta",
    EXPERIMENTS_DIR / "exp_gamma",
]

# -----------------------------------------------------------------------------
# Expected files + their exact byte content (note the trailing \n on each line)
# -----------------------------------------------------------------------------
ARTIFACT_FILES_AND_CONTENT = {
    EXPERIMENTS_DIR / "exp_alpha" / "artifacts.txt": (
        "model_alpha_v1.pt\n"
        "metrics_alpha_v1.json\n"
        "config_alpha.yml\n"
    ),
    EXPERIMENTS_DIR / "exp_beta" / "artifacts.txt": (
        "model_beta_v2.pt\n"
        "metrics_beta_v2.json\n"
        "config_beta.yml\n"
        "shared_vocab.txt\n"
    ),
    EXPERIMENTS_DIR / "exp_gamma" / "artifacts.txt": (
        "model_gamma_v3.pt\n"
        "metrics_gamma_v3.json\n"
        "config_gamma.yml\n"
        "shared_vocab.txt\n"
    ),
}


# =============================================================================
# Tests
# =============================================================================
def test_expected_directories_exist_and_are_directories():
    """
    Verify that every directory we expect is present and is indeed a directory.
    """
    missing = [d for d in EXPECTED_DIRS if not d.exists()]
    not_dirs = [d for d in EXPECTED_DIRS if d.exists() and not d.is_dir()]

    assert not missing, (
        "The following expected directories are missing:\n" +
        "\n".join(str(p) for p in missing)
    )
    assert not not_dirs, (
        "The following expected directories exist but are **not** directories:\n" +
        "\n".join(str(p) for p in not_dirs)
    )


def test_no_unexpected_experiment_subdirectories():
    """
    Ensure that experiments/ contains exactly the three expected sub-directories,
    nothing more and nothing less.
    """
    expected_names = {"exp_alpha", "exp_beta", "exp_gamma"}
    actual_names = {p.name for p in EXPERIMENTS_DIR.iterdir() if p.is_dir()}

    missing = expected_names - actual_names
    extra = actual_names - expected_names

    assert not missing, (
        "The following experiment directories are missing under "
        f"{EXPERIMENTS_DIR} : {', '.join(sorted(missing))}"
    )
    assert not extra, (
        "Unexpected experiment directories found under "
        f"{EXPERIMENTS_DIR} : {', '.join(sorted(extra))}"
    )


@pytest.mark.parametrize("file_path,expected_content", ARTIFACT_FILES_AND_CONTENT.items())
def test_artifact_files_exist_with_correct_content(file_path: Path, expected_content: str):
    """
    For each artifacts.txt file, verify existence and exact byte-for-byte content.
    """
    assert file_path.exists(), f"Expected file is missing: {file_path}"
    assert file_path.is_file(), f"Path exists but is not a regular file: {file_path}"

    actual_bytes = file_path.read_bytes()
    expected_bytes = expected_content.encode()

    assert actual_bytes == expected_bytes, (
        f"Contents of {file_path} differ from the specification.\n"
        "---- Expected (repr) ----\n"
        f"{repr(expected_content)}\n"
        "----   Actual (repr) ----\n"
        f"{repr(actual_bytes.decode(errors='replace'))}"
    )


def test_summary_directory_and_file_do_not_yet_exist():
    """
    The summary directory and its artifacts_summary.txt file must NOT exist
    before the student runs their command.
    """
    assert not SUMMARY_DIR.exists(), (
        "The directory /home/user/mlops/summary/ already exists, but it should "
        "only be created by the student's solution."
    )
    assert not SUMMARY_FILE.exists(), (
        "The file /home/user/mlops/summary/artifacts_summary.txt already exists, "
        "but it should only be created by the student's solution."
    )