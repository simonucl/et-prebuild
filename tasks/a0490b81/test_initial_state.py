# test_initial_state.py
#
# This pytest suite validates that the environment is ready for the
# student to execute the required curl commands.  It intentionally
# DOES NOT look for /home/user/api_test.log (the expected output of the
# student’s work), in accordance with the grading rules.

import json
import shutil
import sys
import urllib.error
import urllib.request

import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"
GET_POST_1_URL = f"{BASE_URL}/posts/1"
POSTS_COLLECTION_URL = f"{BASE_URL}/posts"

EXPECTED_GET_STATUS = 200
EXPECTED_GET_TITLE = (
    "sunt aut facere repellat provident occaecati excepturi optio reprehenderit"
)

EXPECTED_POST_STATUS = 201
EXPECTED_POST_ID = 101

EXPECTED_HEAD_STATUS = 200
EXPECTED_HEAD_CONTENT_TYPE = "application/json; charset=utf-8"


@pytest.fixture(scope="module")
def opener():
    """Return a urllib opener with a small timeout."""
    return lambda req: urllib.request.urlopen(req, timeout=10)


def test_curl_is_installed():
    """
    Students are instructed to use `curl`; make sure it is present.
    """
    curl_path = shutil.which("curl")
    assert curl_path, "curl binary not found in PATH; it is required for the task."


def test_get_posts_1(opener):
    """
    Ensure the GET request returns the expected status code and title.
    """
    req = urllib.request.Request(GET_POST_1_URL, method="GET")
    try:
        with opener(req) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        pytest.fail(f"GET {GET_POST_1_URL} failed: {exc}")

    assert (
        status == EXPECTED_GET_STATUS
    ), f"Expected status {EXPECTED_GET_STATUS} from GET, got {status}"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail("GET response was not valid JSON.")

    title = data.get("title")
    assert (
        title == EXPECTED_GET_TITLE
    ), f'Expected title "{EXPECTED_GET_TITLE}", got "{title}"'


def test_post_new_item(opener):
    """
    Ensure the POST request returns the expected status code and id.
    According to jsonplaceholder API documentation, the returned id is 101.
    """
    post_payload = {
        "title": "adminCheck",
        "body": "Server maintenance",
        "userId": 42,
    }
    post_data = json.dumps(post_payload).encode("utf-8")

    headers = {"Content-Type": "application/json; charset=utf-8"}

    req = urllib.request.Request(
        POSTS_COLLECTION_URL,
        data=post_data,
        headers=headers,
        method="POST",
    )

    try:
        with opener(req) as resp:
            status = resp.getcode()
            body = resp.read().decode("utf-8")
    except urllib.error.URLError as exc:
        pytest.fail(f"POST {POSTS_COLLECTION_URL} failed: {exc}")

    assert (
        status == EXPECTED_POST_STATUS
    ), f"Expected status {EXPECTED_POST_STATUS} from POST, got {status}"

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        pytest.fail("POST response was not valid JSON.")

    post_id = data.get("id")
    assert (
        post_id == EXPECTED_POST_ID
    ), f"Expected returned id {EXPECTED_POST_ID}, got {post_id}"


def test_head_posts_collection(opener):
    """
    Ensure the HEAD request returns the expected status and content-type.
    """
    # Python <3.8 does not have a dedicated HEAD helper, but Request supports 'method'.
    req = urllib.request.Request(POSTS_COLLECTION_URL, method="HEAD")
    try:
        with opener(req) as resp:
            status = resp.getcode()
            content_type = resp.headers.get("Content-Type")
    except urllib.error.URLError as exc:
        pytest.fail(f"HEAD {POSTS_COLLECTION_URL} failed: {exc}")

    assert (
        status == EXPECTED_HEAD_STATUS
    ), f"Expected status {EXPECTED_HEAD_STATUS} from HEAD, got {status}"

    assert (
        content_type == EXPECTED_HEAD_CONTENT_TYPE
    ), f'Expected Content-Type "{EXPECTED_HEAD_CONTENT_TYPE}", got "{content_type}"'