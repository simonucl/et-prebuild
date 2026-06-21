# test_initial_state.py
#
# Pytest suite that validates the pristine state of the filesystem
# before the student performs any actions.

import os
import stat
from pathlib import Path

import pytest

HOME = Path("/home/user")
K8S_DIR = HOME / "k8s-operator"
LOGS_DIR = K8S_DIR / "logs"
OPERATOR_LOG = LOGS_DIR / "operator.log"
ERRORS_ONLY_LOG = LOGS_DIR / "errors_only.log"

# The exact, canonical contents that must be present in operator.log.
EXPECTED_OPERATOR_LOG_LINES = [
    '2023-08-01T08:30:12Z level=info    msg="Starting controller"\n',
    '2023-08-01T08:30:13Z level=error   code=CM001 ns=default name=app-config   msg="Missing ConfigMap"\n',
    '2023-08-01T08:30:14Z level=warning msg="Retry reconcile"\n',
    '2023-08-01T08:30:15Z level=error   code=SV001 ns=prod    name=web-svc      msg="Service not found"\n',
    '2023-08-01T08:30:16Z level=info    msg="Reconcile complete"\n',
    '2023-08-01T08:30:17Z level=error   code=DEP404 ns=staging name=api-deployment msg="Deployment failed"\n',
    '2023-08-01T08:31:18Z level=info    msg="Starting controller"\n',
    '2023-08-01T08:31:19Z level=error   code=CM001 ns=default name=app-config   msg="Missing ConfigMap"\n',
    '2023-08-01T08:31:20Z level=warning msg="Retry reconcile"\n',
    '2023-08-01T08:31:21Z level=error   code=SV001 ns=prod    name=web-svc      msg="Service not found"\n',
]

@pytest.fixture(scope="module")
def operator_log_content():
    """Read operator.log once per test module."""
    if not OPERATOR_LOG.exists():
        pytest.skip("operator.log is missing; cannot validate contents.")
    return OPERATOR_LOG.read_text(encoding="utf-8", errors="strict").splitlines(keepends=True)


def test_directory_structure_exists():
    assert K8S_DIR.is_dir(), f"Directory {K8S_DIR} is missing."
    assert LOGS_DIR.is_dir(), f"Directory {LOGS_DIR} is missing."
    assert OPERATOR_LOG.is_file(), f"File {OPERATOR_LOG} is missing."

def test_operator_log_permissions():
    stat_result = OPERATOR_LOG.stat()
    mode = stat_result.st_mode & 0o777
    expected_mode = 0o644
    assert mode == expected_mode, (
        f"Expected {OPERATOR_LOG} to have permissions {oct(expected_mode)}, "
        f"but found {oct(mode)}."
    )

def test_operator_log_contents_exact(operator_log_content):
    assert operator_log_content == EXPECTED_OPERATOR_LOG_LINES, (
        f"{OPERATOR_LOG} contents do not match the expected baseline.\n"
        "If the file was modified, restore it to the original state before running your solution."
    )

def test_errors_only_log_should_not_exist_yet():
    assert not ERRORS_ONLY_LOG.exists(), (
        f"{ERRORS_ONLY_LOG} already exists. The output file must be created "
        "by the student's solution, and should not be present beforehand."
    )