# test_initial_state.py
#
# This pytest suite validates that the starting state of the filesystem
# is exactly as expected *before* the student runs any command.
#
# Only the pre-existing artefacts required for the exercise are inspected;
# we intentionally ignore anything the student is expected to create
# (/home/user/release_logs and its contents).
#
# If a test fails, the pytest assertion message will clearly indicate what
# is missing or incorrect.

import os
import stat
import json
import pytest

HOME = "/home/user"
MOCK_DIR = os.path.join(HOME, "mock_endpoints")
RELEASE_INFO = os.path.join(MOCK_DIR, "release_info.json")

@pytest.mark.describe("Pre-existing mock_endpoints directory")
def test_mock_endpoints_dir_exists_and_permissions():
    assert os.path.exists(MOCK_DIR), (
        f"Required directory {MOCK_DIR!r} is missing."
    )
    assert os.path.isdir(MOCK_DIR), (
        f"{MOCK_DIR!r} exists but is not a directory."
    )

    mode = stat.S_IMODE(os.stat(MOCK_DIR).st_mode)
    expected_mode = 0o755
    assert mode == expected_mode, (
        f"{MOCK_DIR!r} permissions are {oct(mode)}, expected {oct(expected_mode)}."
    )

@pytest.mark.describe("Pre-existing release_info.json file")
def test_release_info_json_exists_and_contents():
    assert os.path.exists(RELEASE_INFO), (
        f"Required file {RELEASE_INFO!r} is missing."
    )
    assert os.path.isfile(RELEASE_INFO), (
        f"{RELEASE_INFO!r} exists but is not a regular file."
    )

    mode = stat.S_IMODE(os.stat(RELEASE_INFO).st_mode)
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"{RELEASE_INFO!r} permissions are {oct(mode)}, expected {oct(expected_mode)}."
    )

    # Read the file exactly as-is (binary → decode) to avoid newline translation.
    with open(RELEASE_INFO, "rb") as f:
        raw_bytes = f.read()
    try:
        raw_text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        pytest.fail(f"{RELEASE_INFO!r} is not valid UTF-8: {exc}")  # pragma: no cover

    expected_text = '{"version":"1.5.2","status":"ready"}'
    assert raw_text == expected_text, (
        f"{RELEASE_INFO!r} contents are incorrect.\n"
        f"Expected: {expected_text!r}\n"
        f"Found:    {raw_text!r}"
    )

    # The spec says "no newline at EOF"; confirm that.
    assert not raw_text.endswith("\n"), (
        f"{RELEASE_INFO!r} must not contain a trailing newline."
    )

    # Additionally verify that the JSON is syntactically valid.
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{RELEASE_INFO!r} does not contain valid JSON: {exc}")  # pragma: no cover

    expected_dict = {"version": "1.5.2", "status": "ready"}
    assert data == expected_dict, (
        f"{RELEASE_INFO!r} JSON content differs from expected.\n"
        f"Expected: {expected_dict}\n"
        f"Found:    {data}"
    )