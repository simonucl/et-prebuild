# test_initial_state.py
#
# This pytest file verifies the *initial* state of the filesystem before
# the learner generates `/home/user/incident/unhealthy_containers.log`.
# It checks that:
#   1. The directory `/home/user/incident` exists.
#   2. The input file `/home/user/incident/docker_ps.out` exists **and**
#      its byte-for-byte contents match the expected sample data.
#   3. The output file `/home/user/incident/unhealthy_containers.log`
#      does **not** yet exist.
#
# Only the Python standard library and pytest are used.

from pathlib import Path
import pytest

INCIDENT_DIR = Path("/home/user/incident")
DOCKER_PS_PATH = INCIDENT_DIR / "docker_ps.out"
UNHEALTHY_LOG_PATH = INCIDENT_DIR / "unhealthy_containers.log"

# Exact byte-for-byte content that must already be in docker_ps.out.
# A final trailing newline **is** required.
EXPECTED_DOCKER_PS_CONTENT = (
    "CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS                       PORTS                   NAMES\n"
    "1a2b3c4d5e6f   nginx:1.25     \"/docker-entrypoint.…\"   2 hours ago    Up 2 hours (healthy)         0.0.0.0:8080->80/tcp    web-frontend\n"
    "7e8f9a0b1c2d   redis:7.0      \"docker-entrypoint.s…\"   3 hours ago    Exited (1) 30 minutes ago                            redis-cache\n"
    "3d4e5f6a7b8c   postgres:15    \"docker-entrypoint.s…\"   3 hours ago    Restarting (1) 5 seconds ago 0.0.0.0:5432->5432/tcp db-primary\n"
)


def test_incident_directory_exists():
    """Ensure the /home/user/incident directory exists and is a directory."""
    assert INCIDENT_DIR.exists(), (
        f"Required directory {INCIDENT_DIR} is missing."
    )
    assert INCIDENT_DIR.is_dir(), (
        f"{INCIDENT_DIR} exists but is not a directory."
    )


def test_docker_ps_file_exists_and_matches_expected_content():
    """Verify docker_ps.out exists and its contents match exactly."""
    assert DOCKER_PS_PATH.exists(), (
        f"Input file {DOCKER_PS_PATH} is missing."
    )
    assert DOCKER_PS_PATH.is_file(), (
        f"{DOCKER_PS_PATH} exists but is not a regular file."
    )

    actual_content = DOCKER_PS_PATH.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_DOCKER_PS_CONTENT, (
        "The contents of docker_ps.out do not match the expected initial "
        "sample data. Do NOT modify docker_ps.out before running the task."
    )


def test_unhealthy_log_not_yet_created():
    """The output file should not exist before the learner runs their solution."""
    assert not UNHEALTHY_LOG_PATH.exists(), (
        f"The report file {UNHEALTHY_LOG_PATH} already exists, but it should "
        "only be created by the learner's solution."
    )