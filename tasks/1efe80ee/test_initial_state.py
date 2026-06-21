# test_initial_state.py
#
# This pytest suite verifies that the workspace is clean *before* the student
# carries out the “capacity-audit” task.  None of the deliverable paths
# (directory or files) should exist yet.  Should any of them already be
# present, the test(s) will fail with a clear, actionable message.

from pathlib import Path

BASE_DIR = Path("/home/user/projects/capacity_audit")
EXPECTED_FILES = [
    BASE_DIR / "cpu_snapshot.txt",
    BASE_DIR / "mem_snapshot.txt",
    BASE_DIR / "summary_report.log",
]


def test_capacity_audit_directory_absent():
    """
    The target directory must NOT exist at the start of the exercise.
    A pre-existing directory would indicate that the student (or some
    prior process) has already begun creating deliverables.
    """
    assert not BASE_DIR.exists(), (
        f"The directory {BASE_DIR} already exists. "
        "Start with a clean slate—remove or rename it before proceeding."
    )


def test_snapshot_files_absent():
    """
    None of the required output files should exist yet.  This check guards
    against partially completed or leftover work from earlier runs.
    """
    for fpath in EXPECTED_FILES:
        assert not fpath.exists(), (
            f"The file {fpath} already exists. "
            "No snapshot or report files should be present before you run the "
            "capacity-audit commands."
        )