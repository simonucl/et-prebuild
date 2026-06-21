# test_initial_state.py
#
# This test-suite verifies that the machine is in a PRISTINE state
# *before* the student runs any command for the “venv setup” exercise.
#
# What we expect to be ABSENT right now:
#
#   1. /home/user/csv_project/                (the project directory)
#   2. /home/user/csv_project/.venv/          (the virtual-env)
#   3. /home/user/csv_project/.venv/pyvenv.cfg
#   4. /home/user/venv_setup_status.txt       (the status log)
#
# If any of these artefacts already exist, the tests will fail with a
# clear message so that the learner/author knows the environment is not
# clean and reproducible.

import os
from pathlib import Path
import pytest

HOME = Path("/home/user")
CSV_PROJECT_DIR = HOME / "csv_project"
VENV_DIR = CSV_PROJECT_DIR / ".venv"
PYVENV_CFG = VENV_DIR / "pyvenv.cfg"
STATUS_FILE = HOME / "venv_setup_status.txt"


@pytest.mark.parametrize(
    "path, kind",
    [
        (CSV_PROJECT_DIR, "directory"),
        (VENV_DIR, "directory"),
        (PYVENV_CFG, "file"),
        (STATUS_FILE, "file"),
    ],
)
def test_path_does_not_exist_before_exercise(path: Path, kind: str) -> None:
    """
    Ensure that none of the target artefacts exist *before* the student
    starts the exercise.  A pre-existing artefact would render the task
    trivial and could mask problems in the learner’s solution.
    """
    assert not path.exists(), (
        f"Precondition failure: the {kind} {path} already exists. "
        "The machine must start in a clean state so the learner’s single "
        "command can be validated from scratch."
    )


def test_parent_directory_is_pristine() -> None:
    """
    Confirm that /home/user/ does not already contain any csv_project
    artefacts.  If it does, list them for easier debugging.
    """
    offending = [
        p for p in HOME.iterdir()
        if p.name.startswith("csv_project") or p.name == "venv_setup_status.txt"
    ]
    assert not offending, (
        "Expected /home/user/ to be clean, but found pre-existing paths: "
        + ", ".join(str(p) for p in offending)
    )