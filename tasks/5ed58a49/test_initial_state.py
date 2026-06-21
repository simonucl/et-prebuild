# test_initial_state.py
"""
Pytest suite to verify the *initial* state of the filesystem
before the student begins work on the “mini-operator” task.

Nothing from the final expected layout should exist yet.
"""

from pathlib import Path
import pytest

# Base directory that should NOT exist at the outset.
BASE_DIR = Path("/home/user/kube-operator")

# Every path that must be absent prior to student activity.
PATHS_THAT_MUST_NOT_EXIST = [
    BASE_DIR,
    BASE_DIR / "manifests",
    BASE_DIR / "manifests" / "deployment.yaml",
    BASE_DIR / "manifests" / "service.yaml",
    BASE_DIR / "run_parallel.sh",
    BASE_DIR / "logs",
    BASE_DIR / "logs" / "deployment.yaml.log",
    BASE_DIR / "logs" / "service.yaml.log",
    BASE_DIR / "logs" / "summary.log",
]


@pytest.mark.parametrize("path", PATHS_THAT_MUST_NOT_EXIST)
def test_required_paths_do_not_exist_yet(path: Path):
    """
    Ensure that none of the expected final-state files or directories
    are present before the student performs any action.
    """
    assert not path.exists(), (
        f"Pre-condition failure: {path} should NOT exist before the task starts, "
        "but it is already present."
    )