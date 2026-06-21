# test_initial_state.py
#
# This test-suite validates the *initial* state of the operating system
# and filesystem **before** the student starts working on the release
# task for “capacity-planner”.
#
# The assertions mirror the public description of the repository’s
# starting layout and should *only* fail when something critical is
# missing or already modified.

import csv
from pathlib import Path
import subprocess

import pytest


REPO_ROOT = Path("/home/user/capacity-planner")
LOGS_DIR = REPO_ROOT / "logs"
VERSION_FILE = REPO_ROOT / "VERSION"
CHANGELOG_FILE = REPO_ROOT / "CHANGELOG.md"
GIT_DIR = REPO_ROOT / ".git"


@pytest.fixture(scope="session")
def repo_root():
    if not REPO_ROOT.exists():
        pytest.fail(f"Repository root {REPO_ROOT} is missing")
    return REPO_ROOT


def test_git_repository(repo_root):
    """The project must already be a Git repository with an initial commit."""
    assert GIT_DIR.is_dir(), f"Expected {GIT_DIR} directory to exist"

    # `git rev-parse` returns 0 only inside a git repo.
    result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-parse", "--is-inside-work-tree"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "Directory exists but does not appear to be a Git repo"
    assert result.stdout.strip() == "true", "Git is not reporting a work tree"

    # There should already be at least one commit.
    commit_result = subprocess.run(
        ["git", "-C", str(repo_root), "rev-list", "--count", "HEAD"],
        capture_output=True,
        text=True,
    )
    assert commit_result.returncode == 0, "Unable to count commits in repo"
    assert int(commit_result.stdout.strip()) >= 1, "Repository should have at least one commit"


def test_version_file_exists_and_content():
    """VERSION must exist and contain exactly '1.4.3\\n'."""
    assert VERSION_FILE.is_file(), f"Missing VERSION file at {VERSION_FILE}"

    data = VERSION_FILE.read_bytes()
    assert data == b"1.4.3\n", (
        "VERSION file should contain exactly '1.4.3' followed by a LF newline "
        "(no additional spaces or lines)"
    )


def test_changelog_exists_and_non_empty():
    """CHANGELOG.md must exist so student can prepend new section."""
    assert CHANGELOG_FILE.is_file(), f"Missing CHANGELOG.md at {CHANGELOG_FILE}"

    content = CHANGELOG_FILE.read_text(encoding="utf-8")
    assert content.strip(), "CHANGELOG.md exists but is empty"


def test_logs_directory_and_files_exist():
    """logs/ directory with db.csv and web.csv must be present."""
    assert LOGS_DIR.is_dir(), f"Missing logs directory at {LOGS_DIR}"

    expected_files = {"web.csv", "db.csv"}
    present = {p.name for p in LOGS_DIR.glob("*.csv")}
    missing = expected_files - present
    assert not missing, (
        f"Missing expected CSV files in {LOGS_DIR}: {', '.join(sorted(missing))}"
    )


@pytest.mark.parametrize(
    "filename, expected_peaks",
    [
        ("web.csv", {"cpu_percent": 20, "mem_mb": 110}),
        ("db.csv", {"cpu_percent": 45, "mem_mb": 220}),
    ],
)
def test_csv_contents_and_peaks(filename, expected_peaks):
    """
    Verify that each CSV file has the documented header and that the
    maximum values in the cpu_percent and mem_mb columns match the
    description given in the task.
    """
    file_path = LOGS_DIR / filename
    assert file_path.is_file(), f"Expected file {file_path} to exist"

    with file_path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        # Validate header
        expected_header = ["timestamp", "cpu_percent", "mem_mb"]
        assert reader.fieldnames == expected_header, (
            f"{filename}: Expected header {expected_header}, got {reader.fieldnames}"
        )

        rows = list(reader)
        assert rows, f"{filename} contains no data rows"

        # Collect peaks
        max_cpu = max(int(r["cpu_percent"]) for r in rows)
        max_mem = max(int(r["mem_mb"]) for r in rows)

        assert max_cpu == expected_peaks["cpu_percent"], (
            f"{filename}: expected peak cpu_percent {expected_peaks['cpu_percent']}, "
            f"found {max_cpu}"
        )
        assert max_mem == expected_peaks["mem_mb"], (
            f"{filename}: expected peak mem_mb {expected_peaks['mem_mb']}, "
            f"found {max_mem}"
        )