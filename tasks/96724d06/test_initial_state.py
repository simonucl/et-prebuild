# test_initial_state.py
#
# This pytest suite verifies the *initial* state of the operating system /
# filesystem before the student performs any actions for the deployment-log
# counting task.
#
# It intentionally avoids checking for any of the _output_ artefacts that
# the student is expected to create later (e.g. the metrics directory or the
# updated_count.log file), in compliance with the specification.
#
# Only the Python standard library and pytest are used.

import os
import stat
import pytest


DEPLOY_DIR = "/home/user/deployment"
SERVER_LOG = os.path.join(DEPLOY_DIR, "server.log")


# --------------------------------------------------------------------------- #
# Helper data that represents the ground-truth contents of server.log.
# Each string retains its trailing newline so that .readlines() comparison
# is exact.
# --------------------------------------------------------------------------- #
EXPECTED_LOG_LINES = [
    "[2024-05-01 10:01:03] STARTUP complete\n",
    "[2024-05-01 10:02:17] UPDATED service-A to v1.4.2\n",
    "[2024-05-01 10:03:08] Health-check passed\n",
    "[2024-05-01 10:05:44] UPDATED service-B to v3.2.1\n",
    "[2024-05-01 10:07:09] NOTICE scaling event\n",
    "[2024-05-01 10:10:22] UPDATED cache-layer configuration\n",
    "[2024-05-01 10:12:56] INFO background job started\n",
    "[2024-05-01 10:15:31] UPDATED database schema migration\n",
    "[2024-05-01 10:18:47] WARN high memory usage\n",
    "[2024-05-01 10:20:00] COMPLETED rollout script\n",
    "[2024-05-01 10:21:15] UPDATED monitoring alerts\n",
    "[2024-05-01 10:22:59] SHUTDOWN initiated\n",
]

UPDATED_KEYWORD = "UPDATED"
EXPECTED_UPDATED_COUNT = 5


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_deployment_directory_exists():
    assert os.path.isdir(DEPLOY_DIR), (
        f"Expected deployment directory '{DEPLOY_DIR}' to exist, "
        "but it is missing."
    )


def test_deployment_directory_is_writable():
    # Check that the directory is writable by attempting to stat and using os.access
    assert os.access(DEPLOY_DIR, os.W_OK), (
        f"Directory '{DEPLOY_DIR}' exists but is not writable by the current user."
    )


def test_server_log_exists():
    assert os.path.isfile(SERVER_LOG), (
        f"Expected server log file '{SERVER_LOG}' to exist, but it is missing."
    )


def test_server_log_exact_contents():
    """
    The mission specification enumerates the precise, 12-line content
    of server.log.  We compare byte-for-byte (newline included) to detect
    any accidental tampering.
    """
    with open(SERVER_LOG, "r", encoding="utf-8") as fh:
        actual_lines = fh.readlines()

    assert actual_lines == EXPECTED_LOG_LINES, (
        "The contents of server.log do not match the expected initial state.\n\n"
        "Expected:\n"
        + "".join(EXPECTED_LOG_LINES)
        + "\nActual:\n"
        + "".join(actual_lines)
    )


def test_server_log_updated_count():
    """
    Ensure that exactly five lines contain the literal, case-sensitive
    substring 'UPDATED', as declared in the task description.
    """
    with open(SERVER_LOG, "r", encoding="utf-8") as fh:
        updated_lines = [ln for ln in fh if UPDATED_KEYWORD in ln]

    assert len(updated_lines) == EXPECTED_UPDATED_COUNT, (
        f"Expected {EXPECTED_UPDATED_COUNT} lines containing '{UPDATED_KEYWORD}' "
        f"but found {len(updated_lines)}. Lines found:\n" + "".join(updated_lines)
    )