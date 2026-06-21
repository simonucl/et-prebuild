# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem **before**
# the student makes any changes.  If any of these tests fail it means the
# exercise has not been provisioned correctly.

import os
import stat
from pathlib import Path

import pytest


HOME = Path("/home/user")
API_DEPLOYMENT = HOME / "microservices" / "api" / "deployment.yaml"
WORKER_DIR = HOME / "microservices" / "worker"
TASK_LOG_DIR = HOME / "task_logs"


@pytest.fixture(scope="module")
def deployment_text():
    """Return the text content of deployment.yaml as a list of lines."""
    try:
        text = API_DEPLOYMENT.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        pytest.fail(f"Required file not found: {API_DEPLOYMENT}")
    return text.splitlines()


def test_deployment_yaml_exists_and_permissions():
    """deployment.yaml must exist with correct permissions (0644)."""
    assert API_DEPLOYMENT.exists(), f"{API_DEPLOYMENT} is missing"
    assert API_DEPLOYMENT.is_file(), f"{API_DEPLOYMENT} exists but is not a regular file"

    mode = API_DEPLOYMENT.stat().st_mode & 0o777
    expected_mode = 0o644
    assert (
        mode == expected_mode
    ), f"{API_DEPLOYMENT} should have permissions {oct(expected_mode)}, found {oct(mode)}"


def test_deployment_yaml_initial_content(deployment_text):
    """
    Validate the *initial* (unmodified) content of deployment.yaml.

    We do *not* parse YAML – the checks below are enough to confirm the file
    has not yet been edited.
    """
    text = "\n".join(deployment_text)  # convenient for `in` membership tests

    # 1. Version should still be v1 and must appear exactly twice
    versions = [line.strip() for line in deployment_text if "version:" in line]
    assert versions, "No 'version:' lines found in deployment.yaml"
    v1_lines = [line for line in versions if 'version: "v1"' in line]
    assert (
        len(v1_lines) == 2
    ), "Expected exactly two occurrences of 'version: \"v1\"' in deployment.yaml"

    # No v2 yet
    assert 'version: "v2"' not in text, "deployment.yaml already contains v2 – should still be v1"

    # 2. replicas must still be 2
    assert "replicas: 2" in text, "replicas should be 2 in the initial file"

    # 3. image tag must be v1.3.4
    assert (
        "image: registry.example.com/api:v1.3.4" in text
    ), "Container image should be registry.example.com/api:v1.3.4 in the initial file"

    # 4. env must be an empty list (`env: []`)
    assert "env: []" in text, "Expected 'env: []' (empty env list) in the initial file"

    # 5. Ensure none of the *after*-state strings are already present
    forbidden_snippets = [
        "v2.1.0",
        "- name: LOG_LEVEL",
        'value: "debug"',
        "replicas: 5",
    ]
    for snippet in forbidden_snippets:
        assert (
            snippet not in text
        ), f"deployment.yaml already contains '{snippet}', but it should not yet be modified"


def test_worker_directory_exists_and_is_empty():
    """The worker directory must exist, be a directory, have 0700 perms, and be empty."""
    assert WORKER_DIR.exists(), f"Directory {WORKER_DIR} is missing"
    assert WORKER_DIR.is_dir(), f"{WORKER_DIR} exists but is not a directory"

    mode = WORKER_DIR.stat().st_mode & 0o777
    expected_mode = 0o700
    assert (
        mode == expected_mode
    ), f"{WORKER_DIR} should have permissions {oct(expected_mode)}, found {oct(mode)}"

    contents = os.listdir(WORKER_DIR)
    assert (
        contents == []
    ), f"{WORKER_DIR} is expected to be empty initially, but it contains: {contents}"


def test_task_log_directory_absent_initially():
    """The task_logs directory should NOT exist yet."""
    assert not TASK_LOG_DIR.exists(), f"{TASK_LOG_DIR} should not exist before the task starts"