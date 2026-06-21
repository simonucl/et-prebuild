# test_initial_state.py
#
# This pytest suite asserts the *initial* state of the filesystem
# before the student performs any actions.  It must succeed **only**
# when the operating system exactly matches the specification given in
# the task description.

import os
import stat
from pathlib import Path

MICROSERVICES_DIR = Path("/home/user/microservices")
SERVICES_CSV = MICROSERVICES_DIR / "services.csv"
MAPS_DIR = MICROSERVICES_DIR / "maps"
PORT_MAP_JSON = MAPS_DIR / "port-map.json"
TRANSFORM_LOG = MICROSERVICES_DIR / "transform.log"

EXPECTED_CSV_CONTENT = (
    "service_name,image,port\n"
    "auth-service,ghcr.io/org/auth:1.0,8080\n"
    "payment-service,ghcr.io/org/pay:1.0,9090\n"
    "frontend,ghcr.io/org/front:2.1,80\n"
)


def _mode(path: Path) -> int:
    "Return the permission bits of a filesystem object as an int (e.g. 0o755)."
    return stat.S_IMODE(path.lstat().st_mode)


def test_microservices_directory_exists_and_permissions():
    assert MICROSERVICES_DIR.exists(), (
        f"Required directory {MICROSERVICES_DIR} is missing."
    )
    assert MICROSERVICES_DIR.is_dir(), (
        f"{MICROSERVICES_DIR} exists but is not a directory."
    )
    expected_mode = 0o755
    actual_mode = _mode(MICROSERVICES_DIR)
    assert actual_mode == expected_mode, (
        f"{MICROSERVICES_DIR} permissions should be {oct(expected_mode)}, "
        f"found {oct(actual_mode)} instead."
    )


def test_services_csv_exists_content_and_permissions():
    assert SERVICES_CSV.exists(), f"CSV file {SERVICES_CSV} is missing."
    assert SERVICES_CSV.is_file(), f"{SERVICES_CSV} exists but is not a regular file."

    expected_mode = 0o644
    actual_mode = _mode(SERVICES_CSV)
    assert actual_mode == expected_mode, (
        f"{SERVICES_CSV} permissions should be {oct(expected_mode)}, "
        f"found {oct(actual_mode)} instead."
    )

    data = SERVICES_CSV.read_text(encoding="utf-8")
    assert data == EXPECTED_CSV_CONTENT, (
        f"{SERVICES_CSV} content does not match the expected initial CSV.\n"
        "If you have already modified this file, reset it to its original state "
        "before running the tests."
    )


def test_maps_directory_does_not_yet_exist():
    # The 'maps' directory should *not* be present before the student's action.
    assert not MAPS_DIR.exists(), (
        f"Directory {MAPS_DIR} should not exist before the transformation step "
        "is executed."
    )


def test_output_artifacts_do_not_yet_exist():
    # Neither the port-map.json nor transform.log should exist initially.
    assert not PORT_MAP_JSON.exists(), (
        f"Output file {PORT_MAP_JSON} should not exist before the transformation."
    )
    assert not TRANSFORM_LOG.exists(), (
        f"Log file {TRANSFORM_LOG} should not exist before the transformation."
    )