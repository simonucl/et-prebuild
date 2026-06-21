# test_initial_state.py
#
# This pytest suite verifies the operating-system / filesystem state
# *before* the student’s command is executed.

import os
import re
import shutil
import subprocess
from pathlib import Path

import pytest


DOCKER_BINARY = "docker"
EXPECTED_CONTAINER_NAME = "mysql-prod"
EXPECTED_CONTAINER_ID = "87e5c1b4a2d3"
OUTPUT_DIR = Path("/home/user/output")
OUTPUT_FILE = OUTPUT_DIR / "mysql_container_id.log"


def _run_cmd(cmd: list[str]) -> str:
    """
    Helper that runs a shell command and returns stdout as text.
    Fails the test immediately if the command exits with a non-zero code.
    """
    try:
        result = subprocess.run(
            cmd,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Command {' '.join(cmd)!r} failed with exit code {exc.returncode}.\n"
            f"STDOUT:\n{exc.stdout}\nSTDERR:\n{exc.stderr}"
        )
    return result.stdout


@pytest.fixture(scope="module")
def docker_available():
    """
    Ensure the docker CLI is present and accessible.
    """
    docker_path = shutil.which(DOCKER_BINARY)
    assert docker_path, "Docker CLI binary not found in PATH."
    return docker_path


def test_single_mysql_prod_container_running(docker_available):
    """
    The container named 'mysql-prod' must be running, with the exact
    12-character ID specified in the truth data, and **no** additional
    containers with that name may exist.
    """
    # --filter name=... requires '^/name$' to match the full container name
    cmd = [
        DOCKER_BINARY,
        "ps",
        "--filter",
        f"name=^/{EXPECTED_CONTAINER_NAME}$",
        "--format",
        "{{.ID}}",
    ]
    output = _run_cmd(cmd).strip().splitlines()

    assert (
        len(output) == 1
    ), f"Expected exactly one running container named '{EXPECTED_CONTAINER_NAME}', found {len(output)}."

    container_id = output[0].strip()
    assert re.fullmatch(
        r"[0-9a-f]{12}", container_id
    ), f"Retrieved container ID '{container_id}' is not a 12-character hexadecimal string."

    assert (
        container_id == EXPECTED_CONTAINER_ID
    ), f"Expected container ID '{EXPECTED_CONTAINER_ID}', got '{container_id}'."

    # Double-check that the container is indeed running (State.Running == true).
    inspect_output = _run_cmd(
        [DOCKER_BINARY, "inspect", "-f", "{{.State.Running}}", container_id]
    ).strip()
    assert (
        inspect_output.lower() == "true"
    ), f"Container '{EXPECTED_CONTAINER_NAME}' is not in a running state."


def test_output_directory_absent():
    """
    The directory /home/user/output must **not** exist before the student's
    command is run, as per the specification.
    """
    assert (
        not OUTPUT_DIR.exists()
    ), f"Directory {OUTPUT_DIR} should not exist before the task starts."


def test_log_file_absent():
    """
    The log file must not pre-exist; it will be created by the student's
    command.
    """
    assert (
        not OUTPUT_FILE.exists()
    ), f"Log file {OUTPUT_FILE} should not exist before the task starts."