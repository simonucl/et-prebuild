# test_initial_state.py
#
# This test-suite validates the *initial* filesystem state before the
# student carries out any actions for the “status-report package” task.
#
# Expectations:
#   1. /home/user/docs exists.
#   2. outlines.csv & topics.json exist with their exact, unmodified
#      contents.
#   3. /home/user/docs/reports  DOES NOT yet exist, nor do any files
#      that will eventually be created inside it.
#
# If any of these assertions fail, the student’s workspace is not in
# the required starting state and the task cannot be graded reliably.

import csv
import json
import os
import textwrap
import pytest

DOCS_DIR = "/home/user/docs"
OUTLINES_CSV = os.path.join(DOCS_DIR, "outlines.csv")
TOPICS_JSON = os.path.join(DOCS_DIR, "topics.json")
REPORTS_DIR = os.path.join(DOCS_DIR, "reports")

EXPECTED_OUTLINES_CONTENT = textwrap.dedent("""\
    Section,Filename,Status
    Introduction,intro.md,published
    Installation,install.md,draft
    Usage,usage.md,draft
    API,api.md,published
    FAQ,faq.md,draft
    """).strip("\n")

EXPECTED_OUTLINES_ROWS = [
    ("Introduction", "intro.md", "published"),
    ("Installation", "install.md", "draft"),
    ("Usage", "usage.md", "draft"),
    ("API", "api.md", "published"),
    ("FAQ", "faq.md", "draft"),
]

EXPECTED_TOPICS = [
    {"filename": "intro.md", "title": "Project Introduction"},
    {"filename": "install.md", "title": "Installing the Project"},
    {"filename": "usage.md",  "title": "How to Use"},
    {"filename": "api.md",    "title": "API Reference"},
    {"filename": "faq.md",    "title": "Frequently Asked Questions"},
]

OUTPUT_FILES = [
    os.path.join(REPORTS_DIR, "drafts.csv"),
    os.path.join(REPORTS_DIR, "summary.json"),
    os.path.join(REPORTS_DIR, "action.log"),
]


def test_docs_directory_exists_and_is_directory():
    assert os.path.isdir(DOCS_DIR), (
        f"Required directory {DOCS_DIR} is missing or not a directory."
    )


def test_outlines_csv_exists_and_content_is_pristine():
    assert os.path.isfile(OUTLINES_CSV), f"{OUTLINES_CSV} is missing."
    with open(OUTLINES_CSV, newline="") as fp:
        reader = csv.reader(fp)
        rows = list(reader)

    header = rows[0]
    assert header == ["Section", "Filename", "Status"], (
        f"Header mismatch in {OUTLINES_CSV}: {header}"
    )
    body = [tuple(r) for r in rows[1:]]
    assert body == EXPECTED_OUTLINES_ROWS, (
        f"Content of {OUTLINES_CSV} has been modified.\n"
        f"Expected rows:\n{EXPECTED_OUTLINES_ROWS}\n"
        f"Found rows:\n{body}"
    )


def test_topics_json_exists_and_content_is_pristine():
    assert os.path.isfile(TOPICS_JSON), f"{TOPICS_JSON} is missing."
    with open(TOPICS_JSON) as fp:
        data = json.load(fp)

    assert isinstance(data, list), f"{TOPICS_JSON} should contain a JSON list."
    assert data == EXPECTED_TOPICS, (
        f"Content of {TOPICS_JSON} has been modified.\n"
        f"Expected:\n{EXPECTED_TOPICS}\nFound:\n{data}"
    )


def test_reports_directory_does_not_exist_yet():
    assert not os.path.exists(REPORTS_DIR), (
        f"{REPORTS_DIR} already exists, but it must NOT exist before the "
        "student performs the task."
    )


@pytest.mark.parametrize("filepath", OUTPUT_FILES)
def test_output_files_do_not_exist_yet(filepath):
    assert not os.path.exists(filepath), (
        f"Unexpected file {filepath} already exists. No output files should be "
        "present before the task is performed."
    )