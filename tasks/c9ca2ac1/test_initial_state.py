# test_initial_state.py
#
# This pytest suite validates the filesystem *before* the student’s solution
# runs.  It asserts that the initial experiment artifacts are present and that
# the security-scan output directory does **not** yet exist.  Any failure here
# signals that the grading environment itself is inconsistent with the task
# description—not that the student’s code is wrong.

import os
import json
from pathlib import Path

EXPERIMENTS_DIR = Path("/home/user/experiments")
RUN_01 = EXPERIMENTS_DIR / "run_01"
RUN_02 = EXPERIMENTS_DIR / "run_02"

EXPECTED_FILES = {
    RUN_01 / "config.env",
    RUN_01 / "notes.txt",
    RUN_02 / "config.env",
    RUN_02 / "metrics.json",
}

SECURITY_SCAN_DIR = Path("/home/user/security_scan")


def test_experiments_directory_exists():
    assert EXPERIMENTS_DIR.is_dir(), (
        f"Expected directory {EXPERIMENTS_DIR} to exist, "
        "but it is missing or not a directory."
    )


def test_runs_directories_exist():
    for run_dir in (RUN_01, RUN_02):
        assert run_dir.is_dir(), (
            f"Expected experiment sub-directory {run_dir} to exist, "
            "but it is missing or not a directory."
        )


def test_expected_files_exist_and_no_extras():
    actual_files = {Path(root) / name
                    for root, _, files in os.walk(EXPERIMENTS_DIR)
                    for name in files}

    missing = EXPECTED_FILES - actual_files
    extras = actual_files - EXPECTED_FILES

    assert not missing, (
        "The following required files are missing under "
        f"{EXPERIMENTS_DIR}:\n" + "\n".join(sorted(map(str, missing)))
    )
    assert not extras, (
        "Found unexpected files under "
        f"{EXPERIMENTS_DIR}:\n" + "\n".join(sorted(map(str, extras)))
    )


def test_run01_config_contents():
    cfg = RUN_01 / "config.env"
    content = cfg.read_text(encoding="utf-8").splitlines()
    expected = ["DB_PASSWORD=mydbpw", "SECRET_KEY=abc123xyz"]
    assert content == expected, (
        f"File {cfg} does not contain the expected two lines:\n"
        f"Expected: {expected}\nActual:   {content}"
    )


def test_run01_notes_contents():
    notes = RUN_01 / "notes.txt"
    expected_lines = [
        "Training accuracy reached 0.93",
        "Need to regenerate data",
    ]
    content = notes.read_text(encoding="utf-8").splitlines()
    assert content == expected_lines, (
        f"File {notes} does not contain the expected content.\n"
        f"Expected lines: {expected_lines}\nActual lines:   {content}"
    )


def test_run02_config_contents():
    cfg = RUN_02 / "config.env"
    expected_lines = [
        "API_TOKEN=notasecret",
        "ENDPOINT=https://api.internal",
    ]
    content = cfg.read_text(encoding="utf-8").splitlines()
    assert content == expected_lines, (
        f"File {cfg} does not contain the expected content.\n"
        f"Expected lines: {expected_lines}\nActual lines:   {content}"
    )


def test_run02_metrics_json_is_valid():
    metrics_file = RUN_02 / "metrics.json"
    try:
        data = json.loads(metrics_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        pytest.fail(f"File {metrics_file} is not valid JSON: {e}")

    assert data == {"loss": 0.123, "accuracy": 0.932}, (
        f"Unexpected JSON content in {metrics_file}: {data}"
    )


def test_security_scan_directory_absent():
    assert not SECURITY_SCAN_DIR.exists(), (
        f"Directory {SECURITY_SCAN_DIR} should NOT exist before the student "
        "runs their solution, but it is already present."
    )