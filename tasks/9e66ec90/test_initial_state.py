# test_initial_state.py
#
# This pytest test-suite validates the _initial_ filesystem state that should
# exist **before** the student runs the single-line shell command described in
# the task.  It makes sure that:
#
# 1. The pre-created template and .env files are present with the exact
#    byte-for-byte contents expected.
# 2. No rendered manifest or log file is present yet.
# 3. The necessary directory structure up to /home/user/k8s exists.
#
# Any mismatch will surface as a clear pytest failure explaining what is wrong.

import os
from pathlib import Path

import pytest


HOME = Path("/home/user")
K8S_DIR = HOME / "k8s"
TEMPLATE_FILE = K8S_DIR / "templates" / "deployment.yaml.tpl"
ENV_FILE = K8S_DIR / "env" / ".env"
RENDERED_FILE = K8S_DIR / "rendered" / "deployment.yaml"
LOG_FILE = K8S_DIR / "logs" / "render.log"


@pytest.fixture(scope="module")
def expected_template_content() -> str:
    """Return the exact content the template file must have (including newline)."""
    return (
        "apiVersion: apps/v1\n"
        "kind: Deployment\n"
        "metadata:\n"
        "  name: ${APP_NAME}\n"
        "spec:\n"
        "  replicas: 1\n"
        "  selector:\n"
        "    matchLabels:\n"
        "      app: ${APP_NAME}\n"
        "  template:\n"
        "    metadata:\n"
        "      labels:\n"
        "        app: ${APP_NAME}\n"
        "    spec:\n"
        "      containers:\n"
        "        - name: ${APP_NAME}\n"
        '          image: "docker.io/library/${APP_NAME}:${IMAGE_TAG}"\n'
        "          env:\n"
        "            - name: ENVIRONMENT\n"
        "              value: ${ENVIRONMENT}\n"
    )


@pytest.fixture(scope="module")
def expected_env_content() -> str:
    """Return the exact content the .env file must have (including newline)."""
    return (
        "APP_NAME=myapp\n"
        "IMAGE_TAG=v1.2.3\n"
        "ENVIRONMENT=production\n"
    )


def test_directory_structure_exists():
    """All expected directories must exist before any action is taken."""
    for path in [
        K8S_DIR,
        K8S_DIR / "templates",
        K8S_DIR / "env",
    ]:
        assert path.is_dir(), f"Required directory is missing: {path}"


def test_template_file_exists_and_matches(expected_template_content):
    """The deployment template must exist and match the expected byte sequence."""
    assert TEMPLATE_FILE.is_file(), f"Template file missing: {TEMPLATE_FILE}"
    contents = TEMPLATE_FILE.read_text(encoding="utf-8")
    assert (
        contents == expected_template_content
    ), "Template file content does not exactly match the expected initial state."


def test_env_file_exists_and_matches(expected_env_content):
    """The .env file must exist and match the expected byte sequence."""
    assert ENV_FILE.is_file(), f".env file missing: {ENV_FILE}"
    contents = ENV_FILE.read_text(encoding="utf-8")
    assert (
        contents == expected_env_content
    ), ".env file content does not exactly match the expected initial state."


def test_no_rendered_or_log_file_present_yet():
    """Rendered manifest and log should NOT exist before the student runs the one-liner."""
    assert not RENDERED_FILE.exists(), (
        "Rendered manifest already exists before the exercise begins: "
        f"{RENDERED_FILE}"
    )
    assert not LOG_FILE.exists(), (
        "Render log already exists before the exercise begins: "
        f"{LOG_FILE}"
    )