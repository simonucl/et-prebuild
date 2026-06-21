# test_initial_state.py
#
# Pytest suite that validates the initial, unmodified state of the
# filesystem before the student performs the migration task.  It checks
# only the *legacy* input artefacts and never touches or verifies any
# files or directories that will be produced by the student solution.

import os
from pathlib import Path

NGINX_PATH = Path("/home/user/cloud_configs/nginx.yaml")
REDIS_PATH = Path("/home/user/cloud_configs/redis.toml")


# Expected legacy contents (including the single trailing newline).
EXPECTED_LEGACY_NGINX = (
    "apiVersion: v1\n"
    "kind: Service\n"
    "metadata:\n"
    "  name: old-nginx\n"
    "spec:\n"
    "  type: ClusterIP\n"
    "  selector:\n"
    "    app: nginx\n"
    "  ports:\n"
    "    - port: 80\n"
    "      targetPort: 80\n"
)

EXPECTED_LEGACY_REDIS = (
    "[service]\n"
    "name = \"old-redis\"\n"
    "port = 6379\n"
    "replicas = 1\n"
    "\n"
    "[service.resources]\n"
    "memory = \"256Mi\"\n"
    "cpu = \"250m\"\n"
)


def _read_file_text(path: Path) -> str:
    """
    Helper that reads a file as UTF-8 text and raises a clear
    assertion error if the file is missing.
    """
    assert path.is_file(), (
        f"Required legacy file is missing: {path}\n"
        f"Expected to find the unmodified, on-prem configuration file."
    )
    return path.read_text(encoding="utf-8")


def test_legacy_nginx_file_is_present_and_correct():
    """
    The original nginx.yaml must exist and match the exact legacy content.
    """
    content = _read_file_text(NGINX_PATH)
    assert content == EXPECTED_LEGACY_NGINX, (
        "The legacy NGINX configuration file does not contain the expected "
        "pre-migration content.  Ensure the starting state of the repository "
        "is correct before the student begins."
    )


def test_legacy_redis_file_is_present_and_correct():
    """
    The original redis.toml must exist and match the exact legacy content.
    """
    content = _read_file_text(REDIS_PATH)
    assert content == EXPECTED_LEGACY_REDIS, (
        "The legacy Redis configuration file does not contain the expected "
        "pre-migration content.  Ensure the starting state of the repository "
        "is correct before the student begins."
    )