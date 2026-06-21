# test_initial_state.py
#
# This test-suite validates the filesystem *before* the student performs any
# action.  It asserts that the expected input tree exists exactly as described
# in the task statement and that no backup artefacts are present yet.
#
# Do **NOT** edit this file when implementing the task solution.

import os
import time
from pathlib import Path

import pytest

HOME = Path("/home/user")
CONFIGS_ROOT = HOME / "configs"
BACKUP_ROOT = HOME / "configs_recent_backup"

# ------------------------------------------------------------------------------
# Helper data derived from the specification
# ------------------------------------------------------------------------------

EXPECTED_CONF_RELATIVE_PATHS = {
    Path("nginx/nginx.conf"),
    Path("nginx/sites-available/default.conf"),
    Path("app/app.conf"),
    Path("app/db/database.conf"),
    Path("obsolete/old.conf"),
}

# Exact file contents (each with trailing newline)
EXPECTED_CONTENTS = {
    CONFIGS_ROOT / "nginx/nginx.conf": (
        "user  www-data;\n"
        "worker_processes  auto;\n"
        "pid /run/nginx.pid;\n"
    ),
    CONFIGS_ROOT / "nginx/sites-available/default.conf": (
        "server {\n"
        "    listen 80 default_server;\n"
        "    server_name _;\n"
        "    root /var/www/html;\n"
        "}\n"
    ),
    CONFIGS_ROOT / "app/app.conf": (
        "[app]\n"
        "name = SampleApp\n"
        "version = 1.2.3\n"
    ),
    CONFIGS_ROOT / "app/db/database.conf": (
        "[database]\n"
        "host = localhost\n"
        "port = 5432\n"
    ),
    CONFIGS_ROOT / "obsolete/old.conf": "deprecated=true\n",
}

# ------------------------------------------------------------------------------
# Tests
# ------------------------------------------------------------------------------

def test_configs_root_exists_and_is_directory():
    assert CONFIGS_ROOT.exists(), (
        f"Expected directory {CONFIGS_ROOT} is missing."
    )
    assert CONFIGS_ROOT.is_dir(), (
        f"{CONFIGS_ROOT} exists but is not a directory."
    )


def test_backup_root_does_not_exist_yet():
    assert not BACKUP_ROOT.exists(), (
        f"{BACKUP_ROOT} should NOT exist before the student runs the solution."
    )


def test_expected_conf_files_exist_and_no_extras():
    # Collect every .conf file under /home/user/configs
    found_confs = {p.relative_to(CONFIGS_ROOT) for p in CONFIGS_ROOT.rglob("*.conf")}

    missing = EXPECTED_CONF_RELATIVE_PATHS - found_confs
    extra = found_confs - EXPECTED_CONF_RELATIVE_PATHS

    assert not missing, (
        "The following expected .conf files are missing under "
        f"{CONFIGS_ROOT}:\n" + "\n".join(str(CONFIGS_ROOT / m) for m in sorted(missing))
    )
    assert not extra, (
        "Found unexpected .conf files under "
        f"{CONFIGS_ROOT}:\n" + "\n".join(str(CONFIGS_ROOT / e) for e in sorted(extra))
    )


@pytest.mark.parametrize("file_path,expected_content", EXPECTED_CONTENTS.items())
def test_file_contents_are_exact(file_path: Path, expected_content: str):
    assert file_path.exists(), f"Expected file {file_path} is missing."

    actual = file_path.read_text()
    assert actual == expected_content, (
        f"Content mismatch in {file_path}.\n"
        "----- expected -----\n"
        f"{expected_content}"
        "-----   found  -----\n"
        f"{actual}"
    )


def test_modification_times_within_expected_ranges():
    """
    • nginx.conf, default.conf, app.conf, database.conf  :  < 30 days old
    • obsolete/old.conf                                 :  > 30 days old
    """
    now = time.time()
    thirty_days = 30 * 24 * 60 * 60  # seconds

    recent_paths = {
        CONFIGS_ROOT / "nginx/nginx.conf",
        CONFIGS_ROOT / "nginx/sites-available/default.conf",
        CONFIGS_ROOT / "app/app.conf",
        CONFIGS_ROOT / "app/db/database.conf",
    }
    old_path = CONFIGS_ROOT / "obsolete/old.conf"

    for p in recent_paths:
        assert p.exists(), f"Expected recent file {p} is missing."
        age = now - p.stat().st_mtime
        assert age < thirty_days, (
            f"{p} should be newer than 30 days (age={age/86400:.1f} days)."
        )

    assert old_path.exists(), f"Expected old file {old_path} is missing."
    old_age = now - old_path.stat().st_mtime
    assert old_age > thirty_days, (
        f"{old_path} should be older than 30 days (age={old_age/86400:.1f} days)."
    )