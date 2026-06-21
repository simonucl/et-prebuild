# test_initial_state.py
"""
Pytest suite that validates the *initial* filesystem state
before the student starts working on the “web-access log” task.

Checks performed:
1. The raw log file exists **and** its content is exactly what the grader expects.
2. The /home/user/project/cleaned/ directory does **not** exist yet.
3. No output artefacts that the student is supposed to create are present.
"""

from pathlib import Path
import pytest

# ---------- Constants ---------- #
RAW_LOG_PATH = Path("/home/user/project/logs/raw/web_access_2023-11-05.log")
CLEAN_DIR = Path("/home/user/project/cleaned")
CRITICAL_ERRORS_FILE = CLEAN_DIR / "critical_errors_2023-11-05.log"
SUMMARY_FILE = CLEAN_DIR / "errors_summary_2023-11-05.csv"

# Exact canonical content of the raw log file
EXPECTED_RAW_LOG_CONTENT = (
    "2023-11-05T08:12:01Z 10.0.0.5 GET /api/v1/order 404 NotFound\n"
    "2023-11-05T08:15:34Z 203.0.113.45 GET /api/v1/order 200 OK\n"
    "2023-11-05T09:02:17Z 198.51.100.23 POST /api/v1/order 500 InternalServerError\n"
    "2023-11-05T09:15:42Z 10.10.10.10 GET /api/v1/order 500 InternalServerError\n"
    "2023-11-05T09:20:03Z 203.0.113.45 GET /health 200 OK\n"
    "2023-11-05T10:05:55Z 198.51.100.23 GET /api/v1/order 404 NotFound\n"
    "2023-11-05T10:05:55Z 198.51.100.23 GET /api/v1/order 404 NotFound\n"
    "2023-11-05T11:30:44Z 192.0.2.10 GET /api/v1/order 502 BadGateway\n"
    "2023-11-05T11:45:00Z 172.16.0.8 GET /api/v1/order 403 Forbidden\n"
    "2023-11-05T12:00:12Z 203.0.113.45 GET /reports 404 NotFound\n"
    "2023-11-05T12:05:12Z 203.0.113.45 GET /api/v1/order 403 Forbidden\n"
    "2023-11-05T12:30:00Z 203.0.113.46 GET /api/v1/order 400 BadRequest\n"
    "2023-11-05T12:30:00Z 10.0.0.16 GET /api/v1/order 400 BadRequest\n"
    "2023-11-05T12:45:00Z 198.18.0.1 GET /api/v1/order 200 OK\n"
    "2023-11-05T13:00:00Z 203.0.113.47 POST /api/v1/order 201 Created\n"
    "2023-11-05T13:30:00Z 203.0.113.45 GET /api/v1/order 503 ServiceUnavailable\n"
)

# ---------- Tests ---------- #
def test_raw_log_exists_and_is_correct():
    """
    Ensure the raw log file exists and its exact content matches the
    canonical fixture provided by the assignment.
    """
    assert RAW_LOG_PATH.is_file(), (
        f"Expected raw log file at {RAW_LOG_PATH} was not found."
    )

    actual_content = RAW_LOG_PATH.read_text(encoding="utf-8")
    assert actual_content == EXPECTED_RAW_LOG_CONTENT, (
        "Raw log file content does not match the expected fixture. "
        "Make sure the container was started from a clean base image."
    )


def test_clean_directory_does_not_exist_yet():
    """
    The /home/user/project/cleaned directory should *not* exist before
    the student runs any commands.
    """
    assert not CLEAN_DIR.exists(), (
        f"Directory {CLEAN_DIR} already exists, but it should be created "
        "by the student during the exercise."
    )


@pytest.mark.parametrize("path", [CRITICAL_ERRORS_FILE, SUMMARY_FILE])
def test_no_output_files_present(path: Path):
    """
    Ensure none of the expected output files are present yet.
    """
    assert not path.exists(), (
        f"File {path} already exists. The student task is to create it "
        "during the solution process."
    )