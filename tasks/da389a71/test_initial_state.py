# test_initial_state.py
#
# This pytest suite validates that the *pre-task* operating-system state is
# correct.  It checks that the three micro-service log files exist at the
# correct absolute paths **and** that their contents match the canonical
# ground-truth required for subsequent grading.
#
# NOTE:
# • We purposefully do *not* test for the presence of
#   /home/user/incident_reports/2023-10-05_order_checkout_issue.log because that
#   file must be created by the student as part of the assignment.
# • Only standard-library modules plus pytest are used.

import pathlib
import pytest

BASE_PATH = pathlib.Path("/home/user/microservices")

# Expected ground-truth log contents for each service -------------------------
EXPECTED_LOGS = {
    "auth": [
        "2023-10-05T14:23:05Z INFO  correlation_id=a1b2c message=\"login attempt\"",
        "2023-10-05T14:24:55Z INFO  correlation_id=7e19a message=\"validate token start\"",
        "2023-10-05T14:26:03Z ERROR correlation_id=7e19a message=\"failed to validate token\"",
        "2023-10-05T14:28:00Z INFO  correlation_id=abc123 message=\"refresh token\"",
    ],
    "orders": [
        "2023-10-05T14:24:58Z INFO  correlation_id=7e19a message=\"create order start\"",
        "2023-10-05T14:26:04Z ERROR correlation_id=7e19a message=\"order creation failed: auth error\"",
        "2023-10-05T14:29:59Z INFO  correlation_id=d4f20 message=\"create order start\"",
        "2023-10-05T14:30:10Z ERROR correlation_id=d4f20 message=\"order creation failed: db timeout\"",
    ],
    "payments": [
        "2023-10-05T14:26:05Z ERROR correlation_id=7e19a message=\"payment aborted due to order failure\"",
        "2023-10-05T14:31:00Z INFO  correlation_id=d4f20 message=\"charge start\"",
        "2023-10-05T14:31:02Z ERROR correlation_id=d4f20 message=\"charge failed: upstream order error\"",
    ],
}


# Helper ----------------------------------------------------------------------
def _read_log_lines(path: pathlib.Path):
    """
    Return all non-empty lines in the file with trailing newlines stripped.
    """
    with path.open("r", encoding="utf-8") as fh:
        return [ln.rstrip("\n") for ln in fh if ln.strip()]


# Tests -----------------------------------------------------------------------
def test_base_directory_exists():
    assert BASE_PATH.exists(), f"Required directory {BASE_PATH} is missing."
    assert BASE_PATH.is_dir(), f"{BASE_PATH} exists but is not a directory."


@pytest.mark.parametrize("service", list(EXPECTED_LOGS))
def test_service_directory_exists(service):
    service_dir = BASE_PATH / service
    assert service_dir.exists(), f"Directory {service_dir} is missing."
    assert service_dir.is_dir(), f"{service_dir} exists but is not a directory."


@pytest.mark.parametrize("service,expected_lines", EXPECTED_LOGS.items())
def test_service_log_file_contents(service, expected_lines):
    """
    Validate that <service>/service.log exists and its contents match exactly
    the ground-truth lines defined above.  Any deviation will break the
    subsequent automated grading that relies on these logs.
    """
    log_path = BASE_PATH / service / "service.log"

    # --- File presence -------------------------------------------------------
    assert log_path.exists(), f"Log file {log_path} is missing."
    assert log_path.is_file(), f"{log_path} exists but is not a regular file."

    # --- File readability ----------------------------------------------------
    try:
        actual_lines = _read_log_lines(log_path)
    except Exception as exc:
        pytest.fail(f"Unable to read {log_path}: {exc}")

    # --- Content equality ----------------------------------------------------
    assert (
        actual_lines == expected_lines
    ), (
        f"Contents of {log_path} do not match expected ground-truth.\n"
        f"Expected ({len(expected_lines)} lines):\n{expected_lines}\n"
        f"Actual ({len(actual_lines)} lines):\n{actual_lines}"
    )