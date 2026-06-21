# test_initial_state.py
#
# This test-suite validates that the workspace is clean **before** the student
# starts working on the “package-requirements normalisation” exercise.  The
# two artefacts that the final grader will later inspect MUST NOT exist yet.
#
# If any of them are already present, it means the working directory was not
# properly initialised (or the student accidentally committed the answers
# ahead of time).  In that case we fail early with a clear explanation so
# the learner can reset the environment.

import os
import pytest

HOME = "/home/user"
CI_CD_DIR = os.path.join(HOME, "ci_cd")
PINNED_FILE = os.path.join(CI_CD_DIR, "pinned_requirements_sorted.txt")
AUDIT_FILE = os.path.join(CI_CD_DIR, "logs", "pip_audit.log")

@pytest.mark.parametrize(
    "path,descr",
    [
        (PINNED_FILE, "sorted requirements file"),
        (AUDIT_FILE, "pip audit log"),
    ],
)
def test_target_files_do_not_exist_yet(path: str, descr: str) -> None:
    """
    Ensure that none of the final deliverables are present at the very start
    of the exercise.  A pre-existing file (even with the wrong content) could
    interfere with the learner’s workflow or mask errors they need to fix.
    """
    assert not os.path.exists(
        path
    ), (
        f"The {descr!s} at {path!r} already exists. "
        "The workspace should start completely empty so the student can create "
        "it from scratch.  Please remove the file (or re-initialise the repo) "
        "and run the tests again."
    )