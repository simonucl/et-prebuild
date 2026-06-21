# test_initial_state.py
#
# Pytest suite that validates the **initial** operating-system / filesystem
# state *before* the learner performs any actions for the “research_env”
# exercise.  If any of these tests fail it means the environment is **not**
# clean (someone has already, fully or partially, done the work).

import os
from pathlib import Path

# Base paths used throughout the exercise.
DATASETS_DIR = Path("/home/user/datasets")
VENV_DIR = DATASETS_DIR / "research_env"
VENV_ACTIVATE = VENV_DIR / "bin" / "activate"
REQ_FILE = DATASETS_DIR / "requirements.txt"
INSTALL_LOG = DATASETS_DIR / "research_env_install.log"

# Expected final-state file contents (byte-for-byte).
REQ_FINAL_CONTENT = (
    "numpy==1.24.3\n"
    "pandas==1.5.3\n"
    "matplotlib==3.7.1\n"
)
LOG_FINAL_CONTENT = (
    "PACKAGE_FREEZE_OUTPUT_START\n"
    "matplotlib==3.7.1\n"
    "numpy==1.24.3\n"
    "pandas==1.5.3\n"
    "PACKAGE_FREEZE_OUTPUT_END\n"
)


def test_datasets_directory_present():
    """
    The parent directory /home/user/datasets must exist because the exercise
    tells students that the CSV files are already there.  If this directory is
    missing the test-runner environment itself is broken.
    """
    assert DATASETS_DIR.is_dir(), (
        f"Expected directory {DATASETS_DIR} to exist before the exercise starts."
    )


def test_research_env_directory_absent():
    """
    The virtual-environment directory must NOT exist yet; the student will be
    asked to create it.  If it already exists we cannot guarantee the student
    actually performed the required steps.
    """
    assert not VENV_DIR.exists(), (
        f"Found {VENV_DIR} but it should NOT exist before the student runs "
        "python - m venv research_env."
    )


def test_research_env_activate_script_absent():
    """
    The activate script inside the venv obviously cannot exist if the venv
    directory itself is absent.  If it does exist, the environment is not
    clean.
    """
    assert not VENV_ACTIVATE.exists(), (
        f"Found {VENV_ACTIVATE} but the virtual environment must not be present "
        "before the student creates it."
    )


def test_requirements_txt_not_final_state():
    """
    Either /home/user/datasets/requirements.txt does *not* exist yet, or it
    exists but does NOT match the exact three-line specification the student
    will later create.  Both situations are acceptable in the initial state.
    A failure means the required file already contains the final-state
    contents, which would give the student an unfair head start.
    """
    if not REQ_FILE.exists():
        # File absent -> environment is clean for this item.
        return

    actual = REQ_FILE.read_text(encoding="utf-8")
    assert actual != REQ_FINAL_CONTENT, (
        f"{REQ_FILE} already contains the exact required three lines:\n{REQ_FINAL_CONTENT}\n"
        "The initial state should *not* satisfy the final exercise conditions."
    )


def test_install_log_not_final_state():
    """
    /home/user/datasets/research_env_install.log must NOT exist yet, or if it
    does exist it must not exactly match the seven lines required at the end.
    """
    if not INSTALL_LOG.exists():
        return

    actual = INSTALL_LOG.read_text(encoding="utf-8")
    assert actual != LOG_FINAL_CONTENT, (
        f"{INSTALL_LOG} already contains the final expected contents:\n{LOG_FINAL_CONTENT}\n"
        "The install log should not be present (or fully correct) before the student performs the task."
    )