# test_initial_state.py
#
# This pytest suite asserts that the machine is *clean* before the student
# begins the exercise.  In particular, we confirm that:
#   • The working directory and its artefact files do NOT yet exist.
#   • Neither a running (or even stopped) container named “test_web”
#     nor a local image tagged “localweb:1.0” exists.
# If a container runtime (docker or podman) is not available on the
# grader-host, the container-related checks are cleanly skipped.

import os
import subprocess
import shutil
import pytest
from pathlib import Path

HOME = Path("/home/user")
WORKDIR = HOME / "container_work"
DOCKERFILE = WORKDIR / "Dockerfile"
INDEX_HTML = WORKDIR / "index.html"
LOGFILE = WORKDIR / "container_test.log"

#############################
# Helper functions & fixtures
#############################

@pytest.fixture(scope="session")
def container_cli():
    """
    Detect an available container CLI (docker or podman).
    Returns the binary name as a string, or None if neither exists.
    """
    for candidate in ("docker", "podman"):
        if shutil.which(candidate):
            return candidate
    return None


def _run(cli, *args):
    """
    Run `<cli> <args>` and return (exit_code, stdout, stderr)
    without raising.
    """
    result = subprocess.run(
        [cli, *args],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


################
# File-system tests
################

def test_working_directory_absent():
    assert not WORKDIR.exists(), (
        f"The directory {WORKDIR} already exists, but the exercise should "
        "start from a clean state."
    )


@pytest.mark.parametrize("path", [DOCKERFILE, INDEX_HTML, LOGFILE])
def test_artefact_files_absent(path: Path):
    assert not path.exists(), (
        f"The file {path} already exists, but it must be created by the "
        "student during the exercise."
    )

########################
# Container-related tests
########################

def test_no_local_image(container_cli):
    if container_cli is None:
        pytest.skip("No container runtime (docker/podman) available; skipping image check.")

    exit_code, _, _ = _run(container_cli, "image", "inspect", "localweb:1.0")
    assert exit_code != 0, (
        "An image tagged 'localweb:1.0' is already present. "
        "The student is expected to build this image during the exercise, "
        "so it should NOT exist yet."
    )


def test_no_test_web_container(container_cli):
    if container_cli is None:
        pytest.skip("No container runtime (docker/podman) available; skipping container check.")

    # Check for any container (running or stopped) named test_web
    exit_code, stdout, stderr = _run(
        container_cli,
        "ps",
        "-a",               # include stopped containers
        "--filter", "name=test_web",
        "--format", "{{.Names}}",
    )
    assert exit_code == 0, f"Failed to query containers: {stderr}"
    assert "test_web" not in stdout.splitlines(), (
        "A container named 'test_web' already exists. "
        "The student must create (and later remove) this container; "
        "it should NOT be present at the start."
    )


def test_no_running_containers(container_cli):
    if container_cli is None:
        pytest.skip("No container runtime (docker/podman) available; skipping running-containers check.")

    exit_code, stdout, stderr = _run(
        container_cli,
        "ps",               # running containers only
        "--format", "{{.ID}}",
    )
    assert exit_code == 0, f"Failed to list running containers: {stderr}"
    running_ids = [line for line in stdout.splitlines() if line.strip()]
    assert not running_ids, (
        "One or more containers are already running. "
        "The initial state must have *zero* active containers."
    )