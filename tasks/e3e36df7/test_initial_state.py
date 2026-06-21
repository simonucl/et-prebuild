# test_initial_state.py
#
# This pytest suite verifies that the **initial** filesystem
# state is correct *before* the student performs any action.
# It checks only the snapshot file that is provided to the
# student and explicitly avoids touching / validating any of
# the files that the student is expected to create.

from pathlib import Path
import pytest

# Base paths used throughout the tests
HOME = Path("/home/user")
MOCK_DIR = HOME / "mock"
SNAPSHOT_FILE = MOCK_DIR / "docker_ps_output.txt"


@pytest.fixture(scope="module")
def snapshot_text():
    """
    Return the entire text of the snapshot file.
    The fixture will fail early if the file is missing.
    """
    if not SNAPSHOT_FILE.exists():
        pytest.fail(
            f"Required snapshot file is missing:\n  {SNAPSHOT_FILE}\n"
            "Make sure the initial repository clone contains this file."
        )
    if not SNAPSHOT_FILE.is_file():
        pytest.fail(
            f"Expected a regular file at the snapshot path but found something else:\n  {SNAPSHOT_FILE}"
        )
    return SNAPSHOT_FILE.read_text(encoding="utf-8")


def test_mock_directory_exists():
    """Ensure /home/user/mock exists and is a directory."""
    assert MOCK_DIR.exists(), f"Directory missing: {MOCK_DIR}"
    assert MOCK_DIR.is_dir(), f"Expected {MOCK_DIR} to be a directory."


def test_snapshot_file_content(snapshot_text):
    """
    Validate that docker_ps_output.txt contains exactly the expected
    data (including the header line) and ends with a single newline.
    """
    # The precise content we expect in the snapshot file.
    expected = (
        "CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                    NAMES\n"
        "a1b2c3d4e5f6   company/api-gateway     \"docker-entrypoint.sh\"   2 days ago      Up 2 days      0.0.0.0:8080->8080/tcp   api-gateway\n"
        "b2c3d4e5f6a1   company/auth-service    \"docker-entrypoint.sh\"   2 days ago      Up 2 days      0.0.0.0:8081->8081/tcp   auth-service\n"
        "c3d4e5f6a1b2   postgres:13-alpine      \"docker-entrypoint.sh\"   2 days ago      Up 2 days      0.0.0.0:5432->5432/tcp   payments-db\n"
    )

    actual = snapshot_text

    # 1. Exact string comparison
    assert (
        actual == expected
    ), (
        "The contents of /home/user/mock/docker_ps_output.txt do not match the expected "
        "snapshot. If this file was modified or corrupted, the exercise cannot proceed.\n\n"
        "----- Expected -----\n"
        f"{expected}"
        "-----   Got   -----\n"
        f"{actual}"
    )

    # 2. Verify the file ends with exactly one newline character
    assert actual.endswith("\n"), (
        "/home/user/mock/docker_ps_output.txt must end with a single newline character."
    )
    assert not actual.endswith("\n\n"), (
        "Snapshot file contains more than one trailing newline; it should end with exactly one."
    )