# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any actions for the “behavioral_study” dataset-
# organization task.
#
# These tests assert the exact starting conditions described in the
# assignment.  If any test here fails, the initial state of the execution
# environment is wrong and will cause the student’s solution (and the
# downstream grading tests) to mis-behave.
#
# Requirements checked:
#   • /home/user/downloads/ exists.
#   • Exactly three specific *.tsv files are present in that directory:
#       ‑ demographics.tsv
#       ‑ reaction_times.tsv
#       ‑ survey_responses.tsv
#   • No additional *.tsv files are present in /home/user/downloads/.
#   • /home/user/projects/ exists.
#   • /home/user/projects/behavioral_study/ does *not* yet exist.
#
# Only stdlib and pytest are used, and all paths are absolute.

import os
import glob
from pathlib import Path

# --- Constants ----------------------------------------------------------------

HOME_DIR = Path("/home/user").resolve()
DOWNLOADS_DIR = HOME_DIR / "downloads"
PROJECTS_DIR = HOME_DIR / "projects"
BEHAVIORAL_STUDY_DIR = PROJECTS_DIR / "behavioral_study"

EXPECTED_TSV_FILES = {
    "demographics.tsv",
    "reaction_times.tsv",
    "survey_responses.tsv",
}

# --- Helper -------------------------------------------------------------------


def _glob_tsv(directory: Path):
    """
    Return a list of absolute Path objects for *.tsv files located directly
    inside `directory` (non-recursive).
    """
    pattern = str(directory / "*.tsv")
    return [Path(p).resolve() for p in glob.glob(pattern)]


# --- Tests --------------------------------------------------------------------


def test_downloads_directory_exists():
    """/home/user/downloads must exist and be a directory."""
    assert DOWNLOADS_DIR.is_dir(), (
        f"Expected directory {DOWNLOADS_DIR} to exist before the task starts."
    )


def test_expected_tsv_files_present():
    """The three required TSV files must exist inside /home/user/downloads/."""
    missing = [
        fname
        for fname in EXPECTED_TSV_FILES
        if not (DOWNLOADS_DIR / fname).is_file()
    ]
    assert not missing, (
        "The following expected TSV file(s) are missing from "
        f"{DOWNLOADS_DIR}: {', '.join(missing)}"
    )


def test_no_extra_tsv_files_in_downloads():
    """
    Only the three specified TSV files may be present in /home/user/downloads/.
    No additional *.tsv files should be there.
    """
    tsv_paths = _glob_tsv(DOWNLOADS_DIR)
    found_files = {p.name for p in tsv_paths}

    extra = found_files - EXPECTED_TSV_FILES
    missing = EXPECTED_TSV_FILES - found_files

    assert not extra, (
        "Unexpected TSV file(s) found in "
        f"{DOWNLOADS_DIR}: {', '.join(sorted(extra))}"
    )
    assert not missing, (
        "Expected TSV file(s) not found in "
        f"{DOWNLOADS_DIR}: {', '.join(sorted(missing))}"
    )
    assert len(found_files) == 3, (
        f"Exactly three TSV files should be in {DOWNLOADS_DIR}, "
        f"but {len(found_files)} were found."
    )


def test_projects_directory_exists():
    """/home/user/projects must already exist."""
    assert PROJECTS_DIR.is_dir(), (
        f"Expected directory {PROJECTS_DIR} to exist before the task starts."
    )


def test_behavioral_study_directory_absent():
    """
    /home/user/projects/behavioral_study/ should *not* exist yet; the student
    will create it as part of the task.
    """
    assert not BEHAVIORAL_STUDY_DIR.exists(), (
        f"Directory {BEHAVIORAL_STUDY_DIR} should *not* exist before the "
        "student begins the task."
    )