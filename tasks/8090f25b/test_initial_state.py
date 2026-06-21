# test_initial_state.py
#
# Pytest suite that validates the **initial** disk / OS state
# before the student performs any actions required by the task
# description.  All tests rely on Python’s stdlib + pytest only.
#
# If any test here fails, the environment is not in the expected
# starting condition and the exercise cannot be graded fairly.

import os
import tarfile
import pytest
from pathlib import Path


HOME = Path("/home/user").resolve()
PROJECT_ROOT = HOME / "projects" / "microservices"
RESOURCE_DIR = HOME / "resources"
ASSET_TARBALL = RESOURCE_DIR / "assets.tar.gz"

BACKUPS_DIR = HOME / "backups"
BACKUP_LOGS_DIR = HOME / "backup_logs"

# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _read_text(path: Path) -> str:
    """Return file contents as text (strict UTF-8)."""
    return path.read_text(encoding="utf-8")


def _assert_file_contents(path: Path, expected: str) -> None:
    """Assert file exists and has exact contents."""
    assert path.is_file(), f"Expected file at {path} is missing."
    actual = _read_text(path)
    assert actual == expected, (
        f"File {path} has unexpected contents.\n"
        f"Expected:\n{expected!r}\n\nGot:\n{actual!r}"
    )


# ---------------------------------------------------------------------------
# 1. Verify micro-service source trees
# ---------------------------------------------------------------------------

MICROSERVICES = {
    "microserviceA": {
        "app.py":            "print('A')\n",
        "requirements.txt":  "flask==2.0.0\n",
    },
    "microserviceB": {
        "server.js":   "console.log('B');\n",
        "package.json": '{ "name": "B" }\n',
    },
    "microserviceC": {
        "main.go": "package main\nfunc main(){}\n",
        "go.mod":  "module C\n",
    },
}


@pytest.mark.parametrize("service, files", MICROSERVICES.items())
def test_microservice_tree_exists(service, files):
    """Each micro-service directory and its immediate files must exist."""
    svc_dir = PROJECT_ROOT / service
    assert svc_dir.is_dir(), f"Directory {svc_dir} is missing."

    # Immediate files check
    actual_files = sorted(p.name for p in svc_dir.iterdir() if p.is_file())
    expected_files = sorted(files.keys())
    assert (
        actual_files == expected_files
    ), f"{svc_dir} should contain exactly {expected_files}, found {actual_files!r}."

    # Verify contents of each expected file
    for filename, expected_content in files.items():
        _assert_file_contents(svc_dir / filename, expected_content)


# ---------------------------------------------------------------------------
# 2. Verify pre-built asset tarball
# ---------------------------------------------------------------------------

def test_assets_tarball_structure_and_contents():
    """assets.tar.gz must exist and contain the two expected members."""
    assert ASSET_TARBALL.is_file(), f"Tarball {ASSET_TARBALL} is missing."

    expected_members = {
        "./images/logo.png": b"PNGDATA\n",
        "./css/style.css":   b"body{margin:0}\n",
    }

    with tarfile.open(ASSET_TARBALL, "r:gz") as tf:
        names = tf.getnames()
        # The archive must contain exactly the two expected paths (no more, no less)
        assert sorted(names) == sorted(expected_members.keys()), (
            f"{ASSET_TARBALL} should contain only {list(expected_members)}, "
            f"found {names!r}."
        )

        # Verify contents of each member
        for member_name, expected_bytes in expected_members.items():
            member = tf.extractfile(member_name)
            assert member is not None, f"Member {member_name} missing in {ASSET_TARBALL}."
            data = member.read()
            assert data == expected_bytes, (
                f"Member {member_name} in {ASSET_TARBALL} has unexpected contents.\n"
                f"Expected: {expected_bytes!r}\nGot:      {data!r}"
            )


# ---------------------------------------------------------------------------
# 3. Verify that backup-related artefacts do NOT yet exist
# ---------------------------------------------------------------------------

def test_no_backups_or_logs_exist_yet():
    """The exercise starts with no backups, logs, or extracted assets present."""
    # Directories that must not yet exist
    for directory in (BACKUPS_DIR, BACKUP_LOGS_DIR, HOME / "assets"):
        assert not directory.exists(), (
            f"Directory {directory} should NOT exist before the student starts."
        )

    # Backup tarballs must not yet exist
    for svc in MICROSERVICES:
        tarball = BACKUPS_DIR / f"{svc}_20230720.tar.gz"
        assert not tarball.exists(), (
            f"Backup archive {tarball} should not exist yet."
        )

    # Log file must not yet exist
    log_file = BACKUP_LOGS_DIR / "20230720_backup.log"
    assert not log_file.exists(), (
        f"Log file {log_file} should not exist before any actions are taken."
    )