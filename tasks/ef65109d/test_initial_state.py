# test_initial_state.py
"""
Pytest suite that validates the initial state of the filesystem
BEFORE the student’s remediation script is executed.

It checks that the expected Docker snapshot is present and that its
contents list exactly the containers described in the task text.

NOTE:  Do NOT add tests about any output artifacts (restart scripts,
incident logs, etc.).  These belong to the *post-task* validation.
"""
from pathlib import Path
import pytest


SNAPSHOT_PATH = Path("/home/user/ops/docker_ps_2023-10-07T1200.txt")

# Expected identifiers taken from the task description
EXPECTED_CONTAINERS = {
    "d1e3f9c1b2fe": "api_1",
    "b4c2a9d6e7ff": "web_1",
    "f9a4c7d8e9ab": "worker_1",
}


@pytest.fixture(scope="module")
def snapshot_lines():
    """
    Provide the snapshot file split into stripped text lines.

    The fixture will fail early with a clear message if the file is missing.
    """
    if not SNAPSHOT_PATH.exists():
        pytest.fail(
            f"Required snapshot file not found at {SNAPSHOT_PATH}. "
            "Make sure the initial data set is in place."
        )
    if not SNAPSHOT_PATH.is_file():
        pytest.fail(f"{SNAPSHOT_PATH} exists but is not a regular file.")
    # Using universal newlines to be tolerant of different line endings
    return SNAPSHOT_PATH.read_text(encoding="utf-8").splitlines()


def test_snapshot_header_present(snapshot_lines):
    """
    The snapshot must start with the standard `docker ps` header.
    """
    header = next((l for l in snapshot_lines if l.strip()), "")
    assert header.startswith(
        "CONTAINER ID"
    ), "First non-blank line of snapshot should begin with 'CONTAINER ID'."


def test_all_expected_containers_present(snapshot_lines):
    """
    Each expected container ID and its corresponding name must be present
    somewhere in the snapshot file.
    """
    joined = "\n".join(snapshot_lines)

    for cid, name in EXPECTED_CONTAINERS.items():
        assert cid in joined, f"Container ID {cid} missing from snapshot."
        assert name in joined, (
            f"Container name '{name}' (for ID {cid}) missing from snapshot."
        )


def test_exited_container_count(snapshot_lines):
    """
    Exactly two containers should have a STATUS that starts with 'Exited'.
    This mirrors the sample data in the task description and gives the
    student a deterministic number to output (2).
    """
    exited_lines = [
        line
        for line in snapshot_lines
        if " Exited (" in line  # typical docker ps wording: 'Exited (1) ...'
    ]
    assert len(exited_lines) == 2, (
        "Snapshot should contain exactly 2 containers in the 'Exited' state.\n"
        f"Found {len(exited_lines)} such lines instead:\n{exited_lines}"
    )