# test_initial_state.py
#
# This pytest suite validates that the **initial** diagnostic inputs are
# present and exactly match the specification *before* the student starts
# working.  It deliberately avoids looking for any output artefacts such as
# `/home/user/diagnostics/network_summary.log`.

import os
import stat
import pytest
from pathlib import Path

# --------------------------------------------------------------------------- #
# Constants – full, exact paths and byte-for-byte reference contents
# --------------------------------------------------------------------------- #

BASE_DIR = Path("/home/user/diagnostics")
RAW_DIR = BASE_DIR / "raw"

PODS_FILE = RAW_DIR / "pods.txt"
SERVICES_FILE = RAW_DIR / "services.txt"
NODES_FILE = RAW_DIR / "nodes.txt"

EXPECTED_PODS_CONTENT = (
    "NAME                        READY   STATUS              RESTARTS   AGE\n"
    "webapp-74f5d8b6f6-7h8k9     1/1     Running             0          5m\n"
    "webapp-74f5d8b6f6-8i9j0     1/1     Running             0          5m\n"
    "webapp-74f5d8b6f6-l2m3n     0/1     CrashLoopBackOff    3          5m\n"
)

EXPECTED_SERVICES_CONTENT = (
    "NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE\n"
    "webapp-svc   ClusterIP   10.96.0.100     <none>        80/TCP         5m\n"
    "kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP        1d\n"
)

EXPECTED_NODES_CONTENT = (
    "NAME       STATUS     ROLES                  AGE   VERSION\n"
    "master-1   Ready      control-plane,master   25d   v1.24.0\n"
    "worker-1   Ready      worker                 25d   v1.24.0\n"
    "worker-2   Ready      worker                 25d   v1.24.0\n"
)

# Mapping of path -> expected_content so we can parametrise the tests
FILES_AND_CONTENT = {
    PODS_FILE: EXPECTED_PODS_CONTENT,
    SERVICES_FILE: EXPECTED_SERVICES_CONTENT,
    NODES_FILE: EXPECTED_NODES_CONTENT,
}


# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #
def assert_file_mode_readable(path: Path):
    """
    Ensure the file is owner-readable; helps catch permission regressions.
    """
    st = path.stat()
    if not bool(st.st_mode & stat.S_IRUSR):
        pytest.fail(f"{path} exists but is not readable by the current user")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #

@pytest.mark.parametrize("path", [PODS_FILE, SERVICES_FILE, NODES_FILE])
def test_raw_file_exists_and_readable(path: Path):
    """
    Verify that each required raw diagnostic file exists and is readable.
    """
    assert path.is_file(), (
        f"Required input file {path} is missing.\n"
        "Ensure the diagnostic collection step copied the file into place "
        "before running the conversion script."
    )
    assert_file_mode_readable(path)


@pytest.mark.parametrize(
    "path,expected_content",
    list(FILES_AND_CONTENT.items()),
)
def test_raw_file_exact_content(path: Path, expected_content: str):
    """
    The contents of each raw file must **exactly** match what the
    specification describes.  A single byte difference here would cascade
    into incorrect downstream processing, so we enforce a byte-for-byte check.
    """
    actual = path.read_text(encoding="utf-8")
    assert (
        actual == expected_content
    ), (
        f"The contents of {path} do not match the expected reference.\n\n"
        "----- Expected (first 120 chars) -----\n"
        f"{expected_content[:120]!r}\n"
        "----- Actual (first 120 chars)   -----\n"
        f"{actual[:120]!r}\n"
        "Differences here indicate that the starting dataset is not in the "
        "state assumed by the exercise instructions."
    )