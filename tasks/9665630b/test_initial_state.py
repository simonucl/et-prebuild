# test_initial_state.py
#
# Pytest suite that validates the *initial* operating-system / filesystem
# state for the “orders” sequential-scan exercise **before** the student
# runs any command.  These tests must all pass *as delivered*; if they
# fail, the environment is not in the expected clean state.

import os
import subprocess
import shlex
import pytest

QUERY_PLANS_DIR = "/home/user/query_plans"
LOG_FILE = os.path.join(QUERY_PLANS_DIR, "orders_full_scan.log")
CONTAINER_NAME = "pg-optimize"
EXPECTED_IMAGE = "postgres:15"


def _run(cmd: str) -> str:
    """
    Helper to run a shell command and return stdout as str.
    Raises a pytest failure with helpful context on any error.
    """
    try:
        completed = subprocess.run(
            shlex.split(cmd),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True,
        )
    except FileNotFoundError as exc:
        pytest.fail(f"Required binary not found when running '{cmd}': {exc}")
    except subprocess.CalledProcessError as exc:
        pytest.fail(
            f"Command '{cmd}' exited with non-zero status {exc.returncode}.\n"
            f"stdout: {exc.stdout}\nstderr: {exc.stderr}"
        )
    return completed.stdout.strip()


def test_query_plans_directory_exists():
    assert os.path.isdir(
        QUERY_PLANS_DIR
    ), f"Expected directory '{QUERY_PLANS_DIR}' to exist."


def test_log_file_does_not_yet_exist():
    assert not os.path.exists(
        LOG_FILE
    ), f"The log file '{LOG_FILE}' already exists; the student must create it."


def test_container_is_running():
    # `docker ps` with a name filter lists only running containers.
    output = _run(f"docker ps --filter name={CONTAINER_NAME} --format {{.Names}}")
    running_containers = [line.strip() for line in output.splitlines() if line.strip()]
    assert (
        CONTAINER_NAME in running_containers
    ), f"Container '{CONTAINER_NAME}' is not running."


def test_container_image_is_correct():
    output = _run(
        f"docker inspect --format {{.Config.Image}} {CONTAINER_NAME}"
    )
    assert (
        output == EXPECTED_IMAGE
    ), f"Container '{CONTAINER_NAME}' is running image '{output}', expected '{EXPECTED_IMAGE}'."


def test_orders_table_exists_inside_container():
    sql = "SELECT 1 FROM pg_class WHERE relname='orders' AND relkind='r';"
    cmd = (
        f"docker exec {CONTAINER_NAME} "
        f"psql -U postgres -d shop -Atc \"{sql}\""
    )
    output = _run(cmd)
    assert (
        output.strip() == "1"
    ), "Table 'orders' not found in database 'shop' inside the container."