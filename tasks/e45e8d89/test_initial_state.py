# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem layout that must be
# present before the student starts working on the task.  It purposefully
# does NOT check for any of the files or directories that will be generated
# or modified by the student’s solution (e.g. `/home/user/incident_logs/`).
#
# The tests only assert the required starting conditions:
#
# 1. The mock container runtime directory structure exists.
# 2. Both `payment_api` and `web_frontend` containers have a `status.txt`
#    file whose content is the single word “RUNNING” (optionally terminated
#    by a single newline and with no extra whitespace).

from pathlib import Path
import pytest

MOCK_DOCKER_ROOT = Path("/home/user/mock_docker/containers")
CONTAINERS = ["payment_api", "web_frontend"]
STATUS_FILE = "status.txt"
EXPECTED_STATUS = "RUNNING"


def status_file_path(container_name: str) -> Path:
    """Return the absolute pathlib.Path to the status.txt of a container."""
    return MOCK_DOCKER_ROOT / container_name / STATUS_FILE


def read_status(path: Path) -> str:
    """
    Read the status file and return its content with *at most* one trailing
    newline removed, leaving all other characters intact.
    """
    content = path.read_text()
    # Remove a single trailing newline, if present, for comparison.
    return content[:-1] if content.endswith("\n") else content


def assert_no_extra_whitespace(raw_content: str, file_path: Path):
    """
    Assert that the raw content contains no leading/trailing spaces or tabs,
    and does not contain multiple lines.
    """
    assert "\n" not in raw_content.strip("\n"), (
        f"{file_path} must contain exactly one line; found additional newline(s)."
    )
    assert raw_content.strip() == raw_content.rstrip("\n"), (
        f"{file_path} must not contain leading or trailing spaces/tabs."
    )


def test_mock_docker_root_exists_and_is_directory():
    assert MOCK_DOCKER_ROOT.exists(), (
        f"Required directory {MOCK_DOCKER_ROOT} is missing."
    )
    assert MOCK_DOCKER_ROOT.is_dir(), (
        f"{MOCK_DOCKER_ROOT} exists but is not a directory."
    )


@pytest.mark.parametrize("container", CONTAINERS)
def test_container_directory_exists(container):
    container_dir = MOCK_DOCKER_ROOT / container
    assert container_dir.exists(), (
        f"Container directory {container_dir} is missing."
    )
    assert container_dir.is_dir(), (
        f"{container_dir} exists but is not a directory."
    )


@pytest.mark.parametrize("container", CONTAINERS)
def test_status_file_exists(container):
    path = status_file_path(container)
    assert path.exists(), f"Expected status file {path} is missing."
    assert path.is_file(), f"{path} exists but is not a regular file."


@pytest.mark.parametrize("container", CONTAINERS)
def test_status_file_content_is_running(container):
    """
    The status.txt file must contain exactly the word 'RUNNING',
    optionally terminated by a single newline, with no extra whitespace.
    """
    path = status_file_path(container)
    raw_content = path.read_text()
    cleaned_content = read_status(path)
    assert cleaned_content == EXPECTED_STATUS, (
        f"{path} should contain '{EXPECTED_STATUS}', found '{cleaned_content}'."
    )
    assert_no_extra_whitespace(raw_content, path)