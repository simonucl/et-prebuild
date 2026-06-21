# test_initial_state.py
#
# This test-suite validates the state of the filesystem *before* the learner
# carries out the archiving task.  It confirms that the original experiment
# artefacts are present and correct, and that the staging directory for
# archives already exists.  It intentionally does NOT look for (or mention)
# any of the output artefacts that the learner is supposed to create.

from pathlib import Path
import pytest

HOME = Path("/home/user")
EXP_DIR = HOME / "experiments" / "run_01"
ARCHIVES_DIR = HOME / "archives"

# --- Expected artefact details ------------------------------------------------
EXPECTED_FILES = {
    "metrics.json": b'{\n  "accuracy": 0.94,\n  "loss": 0.23\n}\n',
    "model.bin":    b"MODEL_WEIGHTS\n",
    "logs.txt":     b"Training started...\nTraining completed successfully.\n",
}

# ------------------------------------------------------------------------------
def test_experiment_directory_exists_and_has_expected_files():
    """
    The experiment directory must exist and contain *exactly* the three expected
    files (no more, no less).
    """
    assert EXP_DIR.exists(), f"Missing experiment directory: {EXP_DIR}"
    assert EXP_DIR.is_dir(), f"{EXP_DIR} exists but is not a directory"

    present_files = sorted(p.name for p in EXP_DIR.iterdir() if p.is_file())
    expected_files = sorted(EXPECTED_FILES.keys())

    assert present_files == expected_files, (
        "The experiment directory must contain exactly these files:\n"
        f"  {expected_files}\n"
        f"Found:\n"
        f"  {present_files}"
    )

@pytest.mark.parametrize("filename, expected_content", EXPECTED_FILES.items())
def test_file_contents_are_correct(filename, expected_content):
    """
    Each of the three files must contain the exact byte sequence specified in
    the task description (including final new-line characters).
    """
    path = EXP_DIR / filename
    assert path.exists(), f"Expected file is missing: {path}"
    data = path.read_bytes()
    assert data == expected_content, (
        f"Contents of {path} do not match the expected reference.\n"
        "Make sure the initial files have not been modified."
    )

def test_archives_directory_exists():
    """
    The directory that will later hold archives must already exist and be a
    directory.  (Its contents are not checked; the student will populate it.)
    """
    assert ARCHIVES_DIR.exists(), (
        f"Missing directory for archives: {ARCHIVES_DIR}\n"
        "Create it before starting the task."
    )
    assert ARCHIVES_DIR.is_dir(), f"{ARCHIVES_DIR} exists but is not a directory"