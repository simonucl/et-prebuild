# test_initial_state.py
"""
Pytest suite that validates the **initial** state of the operating system
before the student carries out any actions for the “env-demo” exercise.

Nothing related to the target deliverables must exist yet.

If a test fails it means the system is not in the pristine state that the
exercise assumes, and the student would get credit too easily (or be unfairly
penalised) for pre-existing artefacts.
"""

from pathlib import Path
import pytest

# Target paths that must NOT exist at the beginning of the exercise.
BASE_DIR = Path("/home/user/projects/env-demo")
VENV_DIR = BASE_DIR / "venv"
REQUIREMENTS_TXT = BASE_DIR / "requirements.txt"
SETUP_LOG = BASE_DIR / "setup.log"


@pytest.mark.parametrize(
    "path_obj, description",
    [
        (BASE_DIR, "project directory '/home/user/projects/env-demo'"),
        (VENV_DIR, "virtual-environment directory '/home/user/projects/env-demo/venv'"),
        (REQUIREMENTS_TXT, "requirements.txt file '/home/user/projects/env-demo/requirements.txt'"),
        (SETUP_LOG, "setup.log file '/home/user/projects/env-demo/setup.log'"),
    ],
)
def test_artifact_absence(path_obj: Path, description: str):
    """
    Ensure none of the deliverables already exist.

    Students are expected to create these artefacts themselves.  Their presence
    before the exercise starts would invalidate the assessment.
    """
    assert not path_obj.exists(), (
        f"The {description} already exists at {path_obj}. "
        "The initial state should be clean—remove it before proceeding."
    )


def test_parent_directory_exists():
    """
    Sanity-check that the parent directory `/home/user/projects` exists so the student
    can create the `env-demo` folder inside it.  If it does not exist the test
    system itself is misconfigured.
    """
    parent = BASE_DIR.parent
    assert parent.exists(), (
        f"Expected parent directory {parent} to exist so the student can create "
        f"{BASE_DIR.name} inside it, but it was missing."
    )
    assert parent.is_dir(), f"The path {parent} should be a directory."