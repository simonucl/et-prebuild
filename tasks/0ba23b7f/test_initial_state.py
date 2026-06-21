# test_initial_state.py
#
# This pytest suite validates that the *initial* filesystem state required
# for the backup-rotation exercise is present.  Nothing that the student
# script is expected to create is inspected here – only the directories
# and files that must already exist before the task starts.

import os
from pathlib import Path

MICROSERVICES_DIR = Path("/home/user/microservices")

AUTH_DIR = MICROSERVICES_DIR / "auth"
PAYMENT_DIR = MICROSERVICES_DIR / "payment"

# Expected artefacts that MUST exist before the student runs anything.
DIRS_THAT_MUST_EXIST = [
    AUTH_DIR,
    PAYMENT_DIR,
    AUTH_DIR / "logs",
    PAYMENT_DIR / "logs",
]

FILES_THAT_MUST_EXIST = [
    AUTH_DIR / "config.yaml",
    PAYMENT_DIR / "config.yaml",
    AUTH_DIR / "logs" / "app.log",
    AUTH_DIR / "logs" / "error.log",
    PAYMENT_DIR / "logs" / "app.log",
    PAYMENT_DIR / "logs" / "error.log",
]


def _read_text(path: Path) -> str:
    """Helper: safely read small text files."""
    with path.open("r", encoding="utf-8") as fh:
        return fh.read()


def test_required_directories_exist():
    """Verify that all required directories are present."""
    missing_dirs = [d for d in DIRS_THAT_MUST_EXIST if not d.is_dir()]
    assert not missing_dirs, (
        "The following directories are missing but must exist *before* the task "
        f"starts:\n{chr(10).join(str(d) for d in missing_dirs)}"
    )


def test_required_files_exist():
    """Verify that all required files are present."""
    missing_files = [f for f in FILES_THAT_MUST_EXIST if not f.is_file()]
    assert not missing_files, (
        "The following files are missing but must exist *before* the task "
        f"starts:\n{chr(10).join(str(f) for f in missing_files)}"
    )


def test_config_yaml_content_is_intact():
    """Basic sanity check on the config.yaml files so we know they are intact."""
    auth_cfg = _read_text(AUTH_DIR / "config.yaml")
    payment_cfg = _read_text(PAYMENT_DIR / "config.yaml")

    for cfg, name in [(auth_cfg, "auth/config.yaml"), (payment_cfg, "payment/config.yaml")]:
        assert "service_name:" in cfg, f"'service_name:' missing in {name}"
        assert "version:" in cfg, f"'version:' missing in {name}"
        assert "database:" in cfg, f"'database:' block missing in {name}"


def test_log_files_are_non_empty():
    """The existing log files should not be empty so the backup has something to archive."""
    empty_logs = [f for f in FILES_THAT_MUST_EXIST if f.name.endswith(".log") and f.stat().st_size == 0]
    assert not empty_logs, (
        "The following log files are unexpectedly empty; they should contain at least "
        "one line so that a meaningful backup can be produced:\n"
        f"{chr(10).join(str(f) for f in empty_logs)}"
    )