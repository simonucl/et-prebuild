# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state that must be present
# BEFORE the student performs any archiving/deletion work.  Passing this suite
# means the sandbox starts from the correct, known-good baseline.

import os
import pathlib
import hashlib
import pytest

HOME = pathlib.Path("/home/user").resolve()
EXP_DIR = HOME / "experiments"
ARCHIVE_DIR = HOME / "archived_checkpoints"

# --------------------------------------------------------------------------- #
# Helper utilities                                                            #
# --------------------------------------------------------------------------- #
def sha256sum(path: pathlib.Path) -> str:
    """Return the hex sha256 digest of a file (small helper for diagnostics)."""
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Ground-truth specification                                                  #
# --------------------------------------------------------------------------- #
EXPECTED_CKPTS = {
    EXP_DIR / "exp01" / "checkpoints" / "model_epoch_1.ckpt": 19,
    EXP_DIR / "exp01" / "checkpoints" / "model_epoch_2.ckpt": 19,
    EXP_DIR / "exp02" / "checkpoints" / "model_epoch_10.ckpt": 20,
    EXP_DIR / "exp03" / "checkpoints" / "best.ckpt": 21,
}

# --------------------------------------------------------------------------- #
# Tests                                                                       #
# --------------------------------------------------------------------------- #
def test_experiments_directory_present():
    assert EXP_DIR.is_dir(), f"Expected directory {EXP_DIR} is missing."


@pytest.mark.parametrize("ckpt_path,expected_size", EXPECTED_CKPTS.items())
def test_ckpt_files_exist_with_correct_size(ckpt_path: pathlib.Path, expected_size: int):
    assert ckpt_path.is_file(), f"Checkpoint file {ckpt_path} is missing."
    actual_size = ckpt_path.stat().st_size
    assert (
        actual_size == expected_size
    ), (
        f"File {ckpt_path} has size {actual_size} bytes, "
        f"expected {expected_size} bytes. "
        f"SHA256={sha256sum(ckpt_path)}"
    )


def test_no_additional_ckpt_files_exist():
    """Ensure the experiments tree contains *only* the four expected .ckpt files."""
    discovered = {
        pathlib.Path(root) / file
        for root, _, files in os.walk(EXP_DIR)
        for file in files
        if file.endswith(".ckpt")
    }

    missing = EXPECTED_CKPTS.keys() - discovered
    extras = discovered - EXPECTED_CKPTS.keys()

    assert not missing, f"The following expected .ckpt files are missing: {sorted(missing)}"
    assert (
        not extras
    ), f"Found unexpected .ckpt files that should not be present yet: {sorted(extras)}"


def test_archive_directory_absent():
    assert (
        not ARCHIVE_DIR.exists()
    ), f"Archive directory {ARCHIVE_DIR} should NOT exist before the student runs their solution."


def test_no_existing_archive_artifacts():
    tar_path = ARCHIVE_DIR / "ckpt_archive.tar.gz"
    manifest_path = ARCHIVE_DIR / "ckpt_manifest.log"

    assert (
        not tar_path.exists()
    ), f"Tarball {tar_path} must not exist yet — it should be created by the student's solution."
    assert (
        not manifest_path.exists()
    ), f"Manifest {manifest_path} must not exist yet — it should be created by the student's solution."