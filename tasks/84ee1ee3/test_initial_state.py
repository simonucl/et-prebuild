# test_initial_state.py
"""
Pytest suite that validates the initial (pre-task) filesystem state for the
“CPU-limit” Kubernetes compliance exercise.

This file is intended to be executed BEFORE the student performs any action.
It asserts that:
1. The expected directory structure and log files already exist.
2. The log files contain exactly the lines declared in the task description.
3. The Deployment YAML does NOT yet have a `resources:` block.
4. The reports directory exists but is completely empty.
5. No remediation / report files have been created yet.

Any deviation from these expectations will cause a clear, actionable test
failure.
"""
import json
import os
from pathlib import Path

import pytest

# Base paths that will be used throughout the assertions
HOME = Path("/home/user")
CLUSTER_LOGS_DIR = HOME / "cluster_logs"
POLICIES_DIR = HOME / "policies"
REPORTS_DIR = HOME / "reports"

# Fully-qualified paths to the three expected log files
NODE_ALPHA_LOG = CLUSTER_LOGS_DIR / "node-alpha.log"
NODE_BRAVO_LOG = CLUSTER_LOGS_DIR / "node-bravo.log"
NODE_CHARLIE_LOG = CLUSTER_LOGS_DIR / "node-charlie.log"

# Path to the existing Deployment YAML
SECURED_DEPLOYMENT = POLICIES_DIR / "secured-deployment.yaml"

# Paths that SHOULD NOT exist yet
CPU_COMPLIANCE_REPORT = REPORTS_DIR / "cpu_compliance_report.json"
MITIGATION_LOG = REPORTS_DIR / "mitigation.log"

# --------------------------------------------------------------------------- #
# Ground-truth content for each log file, taken verbatim from the task
# description. These strings are used to assert the initial state exactly.
# --------------------------------------------------------------------------- #
NODE_ALPHA_CONTENT = (
    "2024-06-06T08:15:42Z kubelet[987]: Started pod: auth-5d9c8d7cdf-abcde "
    "(cpu_limit=250m)\n"
    "2024-06-06T08:16:10Z kubelet[987]: Started pod: billing-6c8dcbf9f-xyz12 "
    "(cpu_limit=none)\n"
    "2024-06-06T08:16:35Z kubelet[987]: Started pod: payments-7f9d7c9d7f-q2g7x "
    "(cpu_limit=250m)\n"
)

NODE_BRAVO_CONTENT = (
    "2024-06-06T08:20:11Z kubelet[123]: Started pod: cart-7c9d7c9d7f-mnopq "
    "(cpu_limit=none)\n"
    "2024-06-06T08:21:11Z kubelet[123]: Started pod: search-6c8dcbf9f-rstuv "
    "(cpu_limit=250m)\n"
)

NODE_CHARLIE_CONTENT = (
    "2024-06-06T08:25:07Z kubelet[456]: Started pod: catalogue-5d9c8d7cdf-wxyz1 "
    "(cpu_limit=250m)\n"
)

# Mapping from log path → expected content for parametrised tests
EXPECTED_LOG_CONTENT = {
    NODE_ALPHA_LOG: NODE_ALPHA_CONTENT,
    NODE_BRAVO_LOG: NODE_BRAVO_CONTENT,
    NODE_CHARLIE_LOG: NODE_CHARLIE_CONTENT,
}


def _newline_normalised(text: str) -> str:
    """
    Helper that normalises newline style (\r\n vs \n) in a text block.
    Ensures comparisons are robust across operating systems.
    """
    return text.replace("\r\n", "\n")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_directories_exist():
    """Verify that the three main directories exist."""
    assert CLUSTER_LOGS_DIR.is_dir(), (
        f"Expected directory {CLUSTER_LOGS_DIR} is missing."
    )
    assert POLICIES_DIR.is_dir(), (
        f"Expected directory {POLICIES_DIR} is missing."
    )
    assert REPORTS_DIR.is_dir(), (
        f"Expected directory {REPORTS_DIR} is missing."
    )


@pytest.mark.parametrize("log_path,expected_content", EXPECTED_LOG_CONTENT.items())
def test_log_files_present_with_exact_content(log_path: Path, expected_content: str):
    """
    Ensure every *.log file exists and contains exactly (byte-for-byte) the
    declared lines. Any extra or missing line indicates the snapshot was not
    set up correctly.
    """
    assert log_path.is_file(), f"Required log file {log_path} is missing."
    actual = _newline_normalised(log_path.read_text())
    expected = _newline_normalised(expected_content)
    assert (
        actual == expected
    ), f"Content mismatch in {log_path}. Expected:\n{expected}\nGot:\n{actual}"


def test_pod_counts_match_truth_value():
    """
    Parse all log files to confirm that:
      • total_pods == 6
      • non_compliant (cpu_limit=none) == 2
    This guards against any accidental alteration of the provided logs.
    """
    total_pods = 0
    non_compliant = 0

    for path in EXPECTED_LOG_CONTENT:
        for line in _newline_normalised(path.read_text()).strip().splitlines():
            if not line.strip():
                continue  # skip blanks (shouldn't exist but be safe)
            total_pods += 1
            if "cpu_limit=none" in line:
                non_compliant += 1

    assert (
        total_pods == 6
    ), f"Expected exactly 6 pod start events; found {total_pods}."
    assert (
        non_compliant == 2
    ), f"Expected exactly 2 non-compliant pods; found {non_compliant}."


def test_policy_file_initial_state():
    """
    The secured-deployment.yaml should exist but MUST NOT yet contain a
    resources / limits / cpu stanza, i.e. no line containing the string
    'resources:' should be present anywhere.
    """
    assert SECURED_DEPLOYMENT.is_file(), (
        f"Expected policy file {SECURED_DEPLOYMENT} is missing."
    )
    text = SECURED_DEPLOYMENT.read_text()
    forbidden = "resources:"
    assert (
        forbidden not in text
    ), f"Initial policy file already contains '{forbidden}'. It must start without any resources block."


def test_reports_directory_is_empty():
    """
    Prior to student action, the /home/user/reports directory should contain
    no files whatsoever.
    """
    existing_files = [p for p in REPORTS_DIR.iterdir() if p.is_file()]
    assert not existing_files, (
        f"Expected {REPORTS_DIR} to be empty, but the following files were found: "
        f"{', '.join(str(p) for p in existing_files)}"
    )


def test_remediation_and_report_files_do_not_exist_yet():
    """
    CPU compliance JSON report and mitigation log must NOT pre-exist.
    """
    assert not CPU_COMPLIANCE_REPORT.exists(), (
        f"{CPU_COMPLIANCE_REPORT} should NOT exist before the task is started."
    )
    assert not MITIGATION_LOG.exists(), (
        f"{MITIGATION_LOG} should NOT exist before the task is started."
    )