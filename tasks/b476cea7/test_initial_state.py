# test_initial_state.py
#
# Pytest suite that validates the *initial* filesystem/OS state
# before the student executes their one-shot shell command.
#
# Rules enforced:
#   1. /home/user/ci directory must exist.
#   2. /home/user/ci/pipeline_payload.json must exist and its
#      contents must exactly match the expected bytes (including
#      the trailing newline).
#   3. /home/user/ci/validation_summary.txt must NOT exist yet.
#
# Only stdlib + pytest are used.

import json
import os
from pathlib import Path

CI_DIR = Path("/home/user/ci")
PAYLOAD_PATH = CI_DIR / "pipeline_payload.json"
SUMMARY_PATH = CI_DIR / "validation_summary.txt"

# Exact bytes expected inside /home/user/ci/pipeline_payload.json
EXPECTED_PAYLOAD_CONTENT = (
    '{\n'
    '  "pipeline": {\n'
    '    "id": 42,\n'
    '    "status": "succeeded",\n'
    '    "stages": ["build", "test", "deploy"],\n'
    '    "commit": {\n'
    '      "hash": "a1b2c3d4",\n'
    '      "author": "devops"\n'
    '    }\n'
    '  }\n'
    '}\n'
)


def test_ci_directory_exists():
    assert CI_DIR.is_dir(), (
        f"Required directory '{CI_DIR}' is missing. "
        "The CI payload should live under this path."
    )


def test_pipeline_payload_exists():
    assert PAYLOAD_PATH.is_file(), (
        f"Expected artifact '{PAYLOAD_PATH}' not found."
    )


def test_pipeline_payload_exact_content():
    with PAYLOAD_PATH.open("r", encoding="utf-8") as f:
        content = f.read()

    assert content == EXPECTED_PAYLOAD_CONTENT, (
        f"Contents of '{PAYLOAD_PATH}' do not match the expected payload.\n"
        "If you regenerated the JSON, ensure the formatting (indentation, "
        "ordering, and trailing newline) remains EXACTLY as provided."
    )


def test_pipeline_payload_semantics():
    # Double-check semantic correctness in addition to byte-for-byte comparison.
    data = json.loads(EXPECTED_PAYLOAD_CONTENT)
    with PAYLOAD_PATH.open("r", encoding="utf-8") as f:
        file_data = json.load(f)

    assert file_data == data, (
        f"JSON structure inside '{PAYLOAD_PATH}' is incorrect. "
        "Expected semantic equivalence with the reference payload."
    )

    # Additional targeted checks for clarity
    pipeline = file_data.get("pipeline", {})
    assert pipeline.get("status") == "succeeded", (
        "The .pipeline.status value should be 'succeeded'."
    )
    assert "deploy" in pipeline.get("stages", []), (
        'The string "deploy" must appear within .pipeline.stages array.'
    )
    assert pipeline.get("id") == 42, (
        "The .pipeline.id value should be 42."
    )


def test_validation_summary_not_present_yet():
    assert not SUMMARY_PATH.exists(), (
        f"File '{SUMMARY_PATH}' should NOT exist in the initial state. "
        "It must only be created by the student's one-shot command."
    )