# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state that must
# exist before the student begins any work.  It makes sure that the three
# YAML service definition files are present with the exact expected
# contents and that the output artefacts (CSV summary + generation log)
# do *not* yet exist.

import os
import stat
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "microstack")

API_YAML_PATH  = os.path.join(BASE_DIR, "api",    "service.yml")
AUTH_YAML_PATH = os.path.join(BASE_DIR, "auth",   "service.yml")
WORK_YAML_PATH = os.path.join(BASE_DIR, "worker", "service.yml")

CSV_PATH  = os.path.join(BASE_DIR, "service_summary.csv")
LOG_PATH  = os.path.join(BASE_DIR, "summary_generation.log")

EXPECTED_YAMLS = {
    API_YAML_PATH: (
        "service: api\n"
        "image: registry.company.com/api-service:2.1.0\n"
        "ports:\n"
        "  - \"8081:80\"\n"
        "environment:\n"
        "  - \"AUTH_ENDPOINT=http://auth:80\"\n"
        "  - \"CACHE_HOST=redis.internal\"\n"
        "  - \"CACHE_PORT=6379\"\n"
    ),
    AUTH_YAML_PATH: (
        "service: auth\n"
        "image: registry.company.com/auth-service:1.4.2\n"
        "ports:\n"
        "  - \"8080:80\"\n"
        "environment:\n"
        "  - \"DB_HOST=db.internal\"\n"
        "  - \"DB_PORT=5432\"\n"
        "  - \"JWT_SECRET=supersecret\"\n"
    ),
    WORK_YAML_PATH: (
        "service: worker\n"
        "image: registry.company.com/worker-service:0.9.3\n"
        "ports:\n"
        "  - \"8082:80\"\n"
        "environment:\n"
        "  - \"QUEUE_HOST=rabbit.internal\"\n"
        "  - \"QUEUE_PORT=5672\"\n"
    ),
}


def _assert_regular_file(path: str):
    """Helper that asserts path exists and is a regular file."""
    assert os.path.exists(path), f"Expected file {path!r} to exist."
    st = os.stat(path)
    assert stat.S_ISREG(st.st_mode), f"Expected {path!r} to be a regular file."


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def test_microstack_directory_structure():
    """Top-level directory and service subdirs must exist."""
    assert os.path.isdir(BASE_DIR), f"Directory {BASE_DIR!r} is missing."

    for sub in ("api", "auth", "worker"):
        subdir = os.path.join(BASE_DIR, sub)
        assert os.path.isdir(subdir), f"Sub-directory {subdir!r} is missing."


@pytest.mark.parametrize("yaml_path", [API_YAML_PATH, AUTH_YAML_PATH, WORK_YAML_PATH])
def test_service_yaml_files_exist_and_are_regular(yaml_path):
    """Each service.yml must exist and be a regular file."""
    _assert_regular_file(yaml_path)


@pytest.mark.parametrize(
    "yaml_path,expected_content",
    list(EXPECTED_YAMLS.items()),
)
def test_service_yaml_contents_exact_match(yaml_path, expected_content):
    """
    Contents of each YAML file must match the specification **exactly**,
    including newlines and indentation.
    """
    actual = _read_file(yaml_path)
    assert actual == expected_content, (
        f"Content mismatch in {yaml_path!r}.\n"
        "------ EXPECTED ------\n"
        f"{expected_content}"
        "------ ACTUAL --------\n"
        f"{actual}"
        "----------------------"
    )


def test_output_files_do_not_yet_exist():
    """
    The CSV summary and generation log must NOT exist before the student
    runs their solution script/commands.
    """
    assert not os.path.exists(CSV_PATH), (
        f"Output file {CSV_PATH!r} is present but should not exist yet."
    )
    assert not os.path.exists(LOG_PATH), (
        f"Output file {LOG_PATH!r} is present but should not exist yet."
    )