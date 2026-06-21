# test_initial_state.py
#
# This test-suite verifies that the starting filesystem is **clean** – i.e.
# none of the directories, files or symbolic links that the assignment
# eventually has to create are present *before* the student begins work.
#
# If any of the listed paths already exist, the environment is not in the
# required initial state and the tests will fail with a clear explanation.
#
# Only modules from the Python standard library and pytest are used.

import os
import pytest
from pathlib import Path

# Base directory for the non-privileged user account.
HOME = Path("/home/user")

# ---------------------------------------------------------------------------
# Paths that MUST **NOT** exist at the beginning of the exercise
# ---------------------------------------------------------------------------

# Directories that will have to be created by the student later on
DIRS_SHOULD_NOT_EXIST = [
    HOME / "cloud_migration",
    HOME / "cloud_migration" / "services",
    HOME / "cloud_migration" / "services" / "auth-service",
    HOME / "cloud_migration" / "services" / "db-service",
    HOME / "cloud_migration" / "services" / "api-service",
    HOME / "cloud_migration" / "migration_logs",
    HOME / "current_services",
]

# Regular files that will have to be created
FILES_SHOULD_NOT_EXIST = [
    HOME / "cloud_migration" / "services" / "auth-service" / "config.yml",
    HOME / "cloud_migration" / "services" / "db-service" / "config.yml",
    HOME / "cloud_migration" / "services" / "api-service" / "config.yml",
    HOME / "cloud_migration" / "migration_logs" / "symlink_audit.log",
]

# Symbolic links that should *not* exist yet
SYMLINKS_SHOULD_NOT_EXIST = [
    HOME / "current_services" / "auth.yaml",
    HOME / "current_services" / "db.yaml",
    HOME / "current_services" / "api.yaml",
    HOME / "current_services" / "all-services",
]

# Combine every path into one sequence of (path, kind) for parametrised tests
ALL_PATHS = (
    [(p, "directory") for p in DIRS_SHOULD_NOT_EXIST]
    + [(p, "file") for p in FILES_SHOULD_NOT_EXIST]
    + [(p, "symlink") for p in SYMLINKS_SHOULD_NOT_EXIST]
)


@pytest.mark.parametrize("path,kind", ALL_PATHS)
def test_path_does_not_exist(path: Path, kind: str):
    """
    Ensure that the path required for the *final* state is absent
    in the *initial* state.
    """
    # Fast-fail if a symlink exists (even if it points nowhere)
    if path.is_symlink():
        pytest.fail(
            f"Unexpected symbolic link exists at {path!s}. "
            f"The initial filesystem must not contain any of the targets."
        )

    # For everything else, plain existence check is enough
    if path.exists():
        pytest.fail(
            f"Unexpected {kind} found at {path!s}. "
            "The initial filesystem must be empty of assignment artefacts."
        )
    # If we reach here, the path does not exist as required for the clean slate.