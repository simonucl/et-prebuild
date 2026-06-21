# test_initial_state.py
#
# This pytest suite validates the **initial** state of the filesystem *before*
# the student performs any action for the Grafana-dashboard exercise.
#
# Rules being verified:
#   • Required directories and files under /home/user/observability/ exist
#     exactly as described.
#   • The “available” directory already contains the two JSON definition files.
#   • The “enabled” directory is empty (no dashboards have been linked yet).
#   • No symlink for net_traffic.json exists yet.
#   • No log file has been created yet.
#
# If any assertion fails, the error message pinpoints precisely what is wrong,
# making it clear to the student what prerequisite item is missing or
# different.

import json
import os
from pathlib import Path

# Base paths used throughout the assertions
HOME = Path("/home/user")
OBS_ROOT = HOME / "observability"
AVAILABLE_DIR = OBS_ROOT / "dashboards" / "available"
ENABLED_DIR = OBS_ROOT / "dashboards" / "enabled"
SYMLINK_PATH = ENABLED_DIR / "net_traffic.json"
LOG_FILE = OBS_ROOT / "link_actions.log"


def _load_json(path: Path):
    """Utility: load JSON content from *path* and return a Python object."""
    with path.open("r", encoding="utf-8") as fp:
        return json.load(fp)


def test_directories_exist():
    """
    Ensure both dashboards/available and dashboards/enabled directories exist.
    """
    assert AVAILABLE_DIR.is_dir(), (
        f"Missing directory: {AVAILABLE_DIR}. The directory containing the "
        "dashboard JSON files must already exist."
    )
    assert ENABLED_DIR.is_dir(), (
        f"Missing directory: {ENABLED_DIR}. The directory that will hold "
        "enabled dashboards must already exist but be empty."
    )


def test_available_json_files_exist_with_correct_content():
    """
    The two JSON dashboard definition files must pre-exist and have the
    expected data.
    """
    # Expected JSON structures
    expected_net_traffic = {
        "title": "Network Traffic",
        "panels": [
            {
                "id": 1,
                "type": "graph",
                "title": "Inbound",
                "targets": [
                    {"expr": "sum(rate(node_network_receive_bytes_total[5m]))"}
                ],
            },
            {
                "id": 2,
                "type": "graph",
                "title": "Outbound",
                "targets": [
                    {"expr": "sum(rate(node_network_transmit_bytes_total[5m]))"}
                ],
            },
        ],
    }
    expected_cpu_load = {
        "title": "CPU Load",
        "panels": [
            {
                "id": 1,
                "type": "graph",
                "title": "Load Average",
                "targets": [{"expr": "node_load1"}],
            }
        ],
    }

    # Paths to check
    net_path = AVAILABLE_DIR / "net_traffic.json"
    cpu_path = AVAILABLE_DIR / "cpu_load.json"

    for name, path in [
        ("net_traffic.json", net_path),
        ("cpu_load.json", cpu_path),
    ]:
        assert path.is_file(), (
            f"Missing file: {path}. The dashboard JSON '{name}' must already "
            "exist in the available directory."
        )

    # Validate JSON content is as expected
    actual_net = _load_json(net_path)
    actual_cpu = _load_json(cpu_path)

    assert (
        actual_net == expected_net_traffic
    ), "Content of net_traffic.json does not match the expected structure."

    assert (
        actual_cpu == expected_cpu_load
    ), "Content of cpu_load.json does not match the expected structure."


def test_enabled_directory_is_empty():
    """
    The 'enabled' directory must exist but contain no files or sub-directories
    before any dashboard is linked.
    """
    contents = [p for p in ENABLED_DIR.iterdir()]
    assert (
        len(contents) == 0
    ), f"The directory {ENABLED_DIR} is expected to be empty, but found: {contents}"


def test_symlink_not_present_yet():
    """
    There must be *no* symlink (or file) named net_traffic.json in the enabled
    directory prior to the student's action.
    """
    assert not SYMLINK_PATH.exists(), (
        f"Unexpected file or symlink present: {SYMLINK_PATH}. The student has "
        "not yet enabled the dashboard, so this path must be absent."
    )


def test_log_file_not_present_yet():
    """
    The log file should not exist before any action is taken.
    """
    assert not LOG_FILE.exists(), (
        f"Unexpected logfile present: {LOG_FILE}. The log should be created "
        "only after the dashboard is enabled."
    )