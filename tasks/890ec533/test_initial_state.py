# test_initial_state.py
#
# This pytest suite validates the initial operating-system / filesystem
# state *before* the student performs any actions.
#
# Expected initial state (truth value):
# 1. /home/user/nginx.conf  ->  file exists, contents == b"server_tokens on;\n"
# 2. /home/user/security_patch.log -> file does *not* exist
#
# If the system does not match these expectations the tests will fail with
# clear messages.

import os
import pytest

NGINX_CONF_PATH = "/home/user/nginx.conf"
PATCH_LOG_PATH = "/home/user/security_patch.log"


def test_nginx_conf_exists_with_correct_content():
    """
    The configuration file must exist and contain exactly
    'server_tokens on;' followed by a single newline.
    """
    assert os.path.isfile(
        NGINX_CONF_PATH
    ), f"Missing configuration file: {NGINX_CONF_PATH}"

    with open(NGINX_CONF_PATH, "rb") as f:
        content = f.read()

    expected = b"server_tokens on;\n"
    assert (
        content == expected
    ), (
        f"{NGINX_CONF_PATH} should contain exactly {expected!r} "
        f"(length {len(expected)}), but found {content!r} (length {len(content)})."
    )

    assert b"server_tokens off;" not in content, (
        f"{NGINX_CONF_PATH} already contains 'server_tokens off;'—"
        "it should only have 'server_tokens on;' prior to patching."
    )


def test_patch_log_does_not_exist():
    """
    The security patch log must *not* exist before the patch
    is applied.  Its presence would indicate the task was
    already completed or the initial state is incorrect.
    """
    assert not os.path.exists(
        PATCH_LOG_PATH
    ), f"Unexpected file present: {PATCH_LOG_PATH} should not exist before patching."