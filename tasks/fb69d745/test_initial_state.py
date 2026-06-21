# test_initial_state.py
#
# This test-suite verifies that the *initial* filesystem state is exactly as
# expected *before* the student performs any dashboard-cleanup actions.

import json
import os
from pathlib import Path

import pytest

HOME = Path("/home/user")
DASHBOARDS_DIR = HOME / "dashboards"

# --------------------------------------------------------------------------- #
# Helper utilities
# --------------------------------------------------------------------------- #
def read_text(path: Path) -> str:
    """Read a file as UTF-8 text and strip trailing newline characters."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read().rstrip("\n")


# --------------------------------------------------------------------------- #
# Existence & non-existence checks
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "path",
    [
        DASHBOARDS_DIR / "prometheus_k8s_legacy.json",
        DASHBOARDS_DIR / "grafana_overview_legacy.json",
        DASHBOARDS_DIR / "service_latency.json",
        DASHBOARDS_DIR / "readme.md",
    ],
)
def test_required_files_exist(path: Path):
    assert path.exists(), f"Expected file {path} to exist, but it is missing."
    assert path.is_file(), f"Expected {path} to be a regular file."


@pytest.mark.parametrize(
    "path",
    [
        HOME / "dashboard_cleanup.log",
        DASHBOARDS_DIR / "archive",
    ],
)
def test_unwanted_paths_do_not_exist_yet(path: Path):
    assert not path.exists(), (
        f"{path} should NOT exist in the initial state, "
        "but it was found on the filesystem."
    )


def test_dashboards_directory_exists():
    assert DASHBOARDS_DIR.exists(), f"Directory {DASHBOARDS_DIR} is missing."
    assert DASHBOARDS_DIR.is_dir(), f"{DASHBOARDS_DIR} is not a directory."


# --------------------------------------------------------------------------- #
# Content verification
# --------------------------------------------------------------------------- #
def test_json_file_contents_are_unchanged():
    expected_json_content = {
        "prometheus_k8s_legacy.json": {"title": "Prometheus K8s Legacy", "version": 1},
        "grafana_overview_legacy.json": {
            "title": "Grafana Overview Legacy",
            "version": 1,
        },
        "service_latency.json": {"title": "Service Latency", "version": 2},
    }

    for filename, expected in expected_json_content.items():
        path = DASHBOARDS_DIR / filename
        try:
            data = json.loads(read_text(path))
        except json.JSONDecodeError as exc:  # pragma: no cover
            pytest.fail(f"File {path} is not valid JSON: {exc}")

        assert (
            data == expected
        ), f"Content mismatch in {path}.\nExpected: {expected}\nFound:    {data}"


def test_readme_content_is_correct():
    readme_path = DASHBOARDS_DIR / "readme.md"
    expected_text = "These dashboards are managed by the observability team."
    actual_text = read_text(readme_path)
    assert (
        actual_text == expected_text
    ), f"readme.md content mismatch.\nExpected: {expected_text!r}\nFound:    {actual_text!r}"