# test_initial_state.py
#
# This test-suite verifies the *initial* filesystem state **before** any
# student actions take place.  Only the resources that are guaranteed to be
# present (and must remain untouched) are asserted here.
#
# Rules obeyed:
# • Uses only stdlib + pytest.
# • Tests rely on absolute paths under /home/user.
# • No output artefacts (e.g. tuned dashboard or log files) are referenced.

from pathlib import Path
import json
import pytest


DASHBOARDS_DIR = Path("/home/user/dashboards")
ORIGINAL_DASHBOARD = DASHBOARDS_DIR / "app_server_dashboard.json"


@pytest.mark.describe("Pre-existing dashboard directory")
def test_dashboards_directory_exists():
    assert DASHBOARDS_DIR.is_dir(), (
        f"Required directory {DASHBOARDS_DIR} is missing. "
        "It must exist before the tuning task is attempted."
    )


@pytest.mark.describe("Original dashboard JSON file")
def test_original_dashboard_file_exists():
    assert ORIGINAL_DASHBOARD.is_file(), (
        f"Required file {ORIGINAL_DASHBOARD} is missing. "
        "The student must start with the provided dashboard file."
    )


@pytest.mark.describe("Original dashboard file content")
def test_original_dashboard_content_intact():
    """
    Validate that the original dashboard matches the exact structure
    and default threshold values expected before any tuning occurs.
    """
    raw_text = ORIGINAL_DASHBOARD.read_text(encoding="utf-8")

    # Parsing validates that the file is well-formed JSON.
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        pytest.fail(f"{ORIGINAL_DASHBOARD} must contain valid JSON. Parse error: {exc}")

    # High-level keys
    assert data.get("dashboard") == "App Server Metrics", (
        f'"dashboard" key must equal "App Server Metrics" in {ORIGINAL_DASHBOARD}'
    )

    panels = data.get("panels")
    assert isinstance(panels, list) and panels, (
        f'"panels" must be a non-empty list in {ORIGINAL_DASHBOARD}'
    )

    # Look for the cpu_usage and memory_usage panels and verify thresholds.
    cpu_panel = next((p for p in panels if p.get("metric") == "cpu_usage"), None)
    mem_panel = next((p for p in panels if p.get("metric") == "memory_usage"), None)

    assert cpu_panel is not None, (
        f'Panel with metric "cpu_usage" is missing from {ORIGINAL_DASHBOARD}'
    )
    assert mem_panel is not None, (
        f'Panel with metric "memory_usage" is missing from {ORIGINAL_DASHBOARD}'
    )

    assert cpu_panel.get("threshold") == 75, (
        f'cpu_usage threshold must be 75 before tuning; found {cpu_panel.get("threshold")}'
    )
    assert mem_panel.get("threshold") == 80, (
        f'memory_usage threshold must be 80 before tuning; found {mem_panel.get("threshold")}'
    )