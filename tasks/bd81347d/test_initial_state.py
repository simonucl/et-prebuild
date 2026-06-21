# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem state before the
# student performs any action for the "Grafana dashboard checksum" exercise.
#
# NOTE: We purposefully avoid touching /home/user/verifications or any files
# that will be produced by the student, to comply with the requirement:
# “DO NOT test for any of the output files or directories.”

import os
import hashlib
import stat
import pytest

DASHBOARD_DIR = "/home/user/dashboards"
DASHBOARD_JSON = os.path.join(DASHBOARD_DIR, "node_exporter.json")
DASHBOARD_SHA256 = os.path.join(DASHBOARD_DIR, "node_exporter.sha256")

EXPECTED_SHA256_LINE = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  node_exporter.json"
)
EXPECTED_HEX_DIGEST = (
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
)


def test_dashboard_directory_exists_and_is_directory():
    """
    Ensure /home/user/dashboards exists and is a directory.
    """
    assert os.path.exists(
        DASHBOARD_DIR
    ), f"Required directory {DASHBOARD_DIR} is missing."
    assert os.path.isdir(
        DASHBOARD_DIR
    ), f"{DASHBOARD_DIR} exists but is not a directory."


def test_node_exporter_json_exists_and_is_empty_file():
    """
    The dashboard JSON file must exist and be a zero-byte regular file.
    """
    assert os.path.exists(
        DASHBOARD_JSON
    ), f"Dashboard file {DASHBOARD_JSON} is missing."

    # Ensure it is a regular file (not a dir, fifo, etc.)
    st = os.stat(DASHBOARD_JSON)
    assert stat.S_ISREG(
        st.st_mode
    ), f"{DASHBOARD_JSON} exists but is not a regular file."

    assert st.st_size == 0, (
        f"{DASHBOARD_JSON} should be an empty file (0 bytes) "
        f"but is {st.st_size} bytes."
    )


def test_sha256_file_exists_and_has_expected_content():
    """
    The .sha256 file must exist and contain the exact expected line.
    """
    assert os.path.exists(
        DASHBOARD_SHA256
    ), f"Checksum file {DASHBOARD_SHA256} is missing."

    st = os.stat(DASHBOARD_SHA256)
    assert stat.S_ISREG(
        st.st_mode
    ), f"{DASHBOARD_SHA256} exists but is not a regular file."
    assert (
        st.st_size > 0
    ), f"Checksum file {DASHBOARD_SHA256} is empty; expected a SHA-256 line."

    with open(DASHBOARD_SHA256, "r", encoding="utf-8") as fh:
        content = fh.read().rstrip("\n")

    assert (
        content == EXPECTED_SHA256_LINE
    ), (
        f"Checksum file content mismatch.\n"
        f"Expected: {EXPECTED_SHA256_LINE!r}\n"
        f"Got     : {content!r}"
    )


def test_sha256_file_matches_actual_json_hash():
    """
    Cross-verify that the hash recorded in the checksum file actually matches
    the SHA-256 digest of the current node_exporter.json file.
    """
    # Compute hash of JSON file
    hasher = hashlib.sha256()
    with open(DASHBOARD_JSON, "rb") as fh:
        # In this specific task the file is empty, but we compute it generically.
        for chunk in iter(lambda: fh.read(8192), b""):
            hasher.update(chunk)
    actual_digest = hasher.hexdigest()

    assert (
        actual_digest == EXPECTED_HEX_DIGEST
    ), (
        "The SHA-256 digest of node_exporter.json does not match the value "
        "recorded in the checksum file.\n"
        f"Expected digest: {EXPECTED_HEX_DIGEST}\n"
        f"Actual digest  : {actual_digest}"
    )