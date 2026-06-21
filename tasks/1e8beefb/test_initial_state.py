# test_initial_state.py
#
# This pytest suite validates that the workspace **before** any student action
# matches the expected pristine state.  It checks:
#
# 1. The original nginx.conf in /home/user/deployment/staging/ is present and
#    byte-for-byte identical to the specification.
# 2. The prod directory exists but does **not** yet contain nginx.conf or
#    optimization.log (or anything else).
#
# Any failure message is written to help the learner immediately see what is
# missing or out of place.

import os
import pytest

STAGING_CONF = "/home/user/deployment/staging/nginx.conf"
PROD_DIR = "/home/user/deployment/prod"
PROD_CONF = "/home/user/deployment/prod/nginx.conf"
PROD_LOG = "/home/user/deployment/prod/optimization.log"

# The exact, byte-for-byte content that must be present in the staging file
EXPECTED_STAGING_CONTENT = (
    "user  nginx;\n"
    "worker_processes  1;\n"
    "\n"
    "events {\n"
    "    worker_connections  1024;\n"
    "}\n"
    "\n"
    "http {\n"
    "    include       mime.types;\n"
    "    default_type  application/octet-stream;\n"
    "\n"
    "    sendfile        on;\n"
    "    keepalive_timeout  65;\n"
    "\n"
    "    server {\n"
    "        listen       80;\n"
    "        server_name  localhost;\n"
    "\n"
    "        location / {\n"
    "            root   /usr/share/nginx/html;\n"
    "            index  index.html index.htm;\n"
    "        }\n"
    "    }\n"
    "}\n"
)


def test_staging_nginx_conf_exists():
    """The original nginx.conf must be present in the staging area."""
    assert os.path.isfile(STAGING_CONF), (
        f"Expected file missing: {STAGING_CONF}. "
        "The task cannot start without the original configuration file."
    )


def test_staging_nginx_conf_contents_are_pristine():
    """
    The staging nginx.conf must be **exactly** the published version.
    This protects against unintended mutations to the source file.
    """
    with open(STAGING_CONF, "r", encoding="utf-8", newline="") as fh:
        actual = fh.read()
    assert actual == EXPECTED_STAGING_CONTENT, (
        "The content of the staging nginx.conf does not match the specification.\n"
        "If this test fails, ensure the file has not been modified:\n"
        f"{STAGING_CONF}"
    )

def test_prod_directory_exists_and_is_empty():
    """
    The prod directory must already exist but be completely empty.
    This guarantees the student starts from a clean slate.
    """
    assert os.path.isdir(PROD_DIR), (
        f"Expected directory missing: {PROD_DIR}. "
        "Create this directory before proceeding with deployment."
    )

    contents = os.listdir(PROD_DIR)
    assert not contents, (
        f"{PROD_DIR} is expected to be empty before deployment, "
        f"but it currently contains: {contents}"
    )

def test_no_prod_nginx_conf_or_log_yet():
    """Ensure the target files do not pre-exist in prod."""
    assert not os.path.exists(PROD_CONF), (
        f"Found unexpected file: {PROD_CONF}. "
        "The prod nginx.conf should be created by the student as part of the task."
    )
    assert not os.path.exists(PROD_LOG), (
        f"Found unexpected file: {PROD_LOG}. "
        "The optimization log should be created by the student as part of the task."
    )