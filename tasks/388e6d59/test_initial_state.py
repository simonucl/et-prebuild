# test_initial_state.py
#
# This test-suite validates the *initial* state of the filesystem before the
# student performs any actions for the “incident-responder certificate” task.
#
# Rules verified:
#   1. The snapshot file /home/user/certs/server_info.txt must exist and match
#      the exact, known-good contents provided in the exercise description.
#   2. No output artefacts from the yet-to-be-written solution should exist.
#      In particular, /home/user/ir_logs/cert_analysis.log must be absent.
#
# If any of these assertions fail, the learner’s environment is not in the
# expected pristine state and the exercise should not continue.

from pathlib import Path

import pytest


CERTS_DIR = Path("/home/user/certs")
SERVER_INFO = CERTS_DIR / "server_info.txt"

IR_LOGS_DIR = Path("/home/user/ir_logs")
CERT_ANALYSIS_LOG = IR_LOGS_DIR / "cert_analysis.log"


EXPECTED_SERVER_INFO_CONTENT = (
    "Subject: CN=www.acme-inc.internal\n"
    "Not Before: Jun 15 00:00:00 2023 GMT\n"
    "Not After : Jun 15 23:59:59 2025 GMT\n"
    "Serial    : 65A9C3\n"
)


def test_server_info_file_present_and_exact():
    """
    The snapshot file must exist *exactly* as provided so that the learner
    can parse it later.
    """
    assert SERVER_INFO.exists(), (
        f"Expected the snapshot file {SERVER_INFO} to exist, "
        "but it is missing."
    )
    assert SERVER_INFO.is_file(), (
        f"{SERVER_INFO} exists but is not a regular file."
    )

    actual_content = SERVER_INFO.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_SERVER_INFO_CONTENT, (
        f"The contents of {SERVER_INFO} do not match the expected value.\n"
        "---- Expected ----\n"
        f"{EXPECTED_SERVER_INFO_CONTENT!r}\n"
        "---- Found ----\n"
        f"{actual_content!r}"
    )


def test_output_log_does_not_exist_yet():
    """
    Before the learner’s solution runs, no output directory or log file
    should be present.
    """
    assert not CERT_ANALYSIS_LOG.exists(), (
        f"Found {CERT_ANALYSIS_LOG} on disk, but the learner has not yet run "
        "their solution. The environment should start clean."
    )