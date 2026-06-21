# test_initial_state.py
#
# This pytest suite validates the **initial** filesystem state _before_ the
# student runs any commands.  It asserts that:
#
# 1. The mock “posts” API payload is present at the expected location and
#    contains the correct JSON structure.
# 2. None of the files that the student is supposed to create (`posts.json`,
#    `post_titles.txt`, `etl_curl.log`) are present yet under
#    /home/user/data.
#
# If any of these assertions fail, the accompanying error message should make
# it immediately obvious what is wrong and why.

import json
from pathlib import Path

import pytest

HOME = Path("/home/user")
MOCK_API_FILE = HOME / "mock_api" / "posts.json"

DATA_DIR = HOME / "data"
OUTPUT_FILES = {
    "downloaded json": DATA_DIR / "posts.json",
    "extracted titles": DATA_DIR / "post_titles.txt",
    "etl log": DATA_DIR / "etl_curl.log",
}


def test_mock_api_payload_exists_and_is_valid_json():
    """
    The seed JSON file that mimics the remote API must exist *before* the
    student starts.  We also validate that its content matches the expected
    structure so that later tests (run after the student’s work) are
    meaningful.
    """
    assert MOCK_API_FILE.exists(), (
        f"Expected seed file {MOCK_API_FILE} to exist, but it is missing.\n"
        "Without this file the exercise cannot be completed."
    )

    # Validate JSON load
    try:
        payload = json.loads(MOCK_API_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        pytest.fail(
            f"Seed file {MOCK_API_FILE} is not valid JSON: {exc}"
        )

    # Expected structure: {"posts": [ { "id": int, "title": str }, ... ]}
    assert isinstance(payload, dict) and "posts" in payload, (
        f"Seed JSON does not contain a top-level 'posts' array. "
        f"Found keys: {list(payload) if isinstance(payload, dict) else 'N/A'}"
    )

    posts = payload["posts"]
    assert isinstance(posts, list) and len(posts) == 3, (
        "Seed JSON 'posts' array must contain exactly three elements."
    )

    expected_titles = ["Build pipelines", "Test ETL", "Deploy to prod"]
    got_titles = [p.get("title") for p in posts]
    assert got_titles == expected_titles, (
        "Seed JSON titles do not match the expected values.\n"
        f"Expected: {expected_titles}\nGot:      {got_titles}"
    )


@pytest.mark.parametrize("description,path_", OUTPUT_FILES.items())
def test_output_files_do_not_exist_yet(description, path_):
    """
    None of the files the student is supposed to create should exist prior to
    execution.  Their presence at this stage would indicate that the initial
    environment is contaminated or that the student has run commands
    prematurely.
    """
    assert not path_.exists(), (
        f"The {description} file should NOT exist yet at {path_}.\n"
        "Make sure the workspace is in its pristine initial state before "
        "running the exercise."
    )