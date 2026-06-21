# test_initial_state.py
#
# This test-suite validates that the brand-new “myapp” project
# has the exact directory tree and file contents required by CI/CD
# *before* any deployment pipeline runs.
#
# To pass, the student must create every path and file **exactly** as
# specified in the task description—nothing more, nothing less.

import os
from pathlib import Path
import pytest

# ---------- CONSTANTS ---------------------------------------------------------

BASE          = Path("/home/user/releases/myapp")
ENV_DIR       = BASE / "env"
DEV_DIR       = ENV_DIR / "development"
STG_DIR       = ENV_DIR / "staging"
PRD_DIR       = ENV_DIR / "production"

ENV_EXAMPLE   = BASE / ".env.example"
DEV_ENV       = DEV_DIR / ".env"
STG_ENV       = STG_DIR / ".env"
PRD_ENV       = PRD_DIR / ".env"

CSV_FILE      = ENV_DIR / "all_envs_summary.csv"
DEPLOY_LOG    = BASE / "deploy_vars.log"

EXPECTED_ENV_EXAMPLE = (
    "DB_HOST=\n"
    "DB_PORT=\n"
    "DB_USER=\n"
    "DB_PASS=\n"
    "API_KEY=\n"
    "LOG_LEVEL=\n"
)

EXPECTED_DEV_ENV = (
    "DB_HOST=localhost\n"
    "DB_PORT=5432\n"
    "DB_USER=devuser\n"
    "DB_PASS=devpass123\n"
    "API_KEY=DEV-23ab9\n"
    "LOG_LEVEL=debug\n"
)

EXPECTED_STG_ENV = (
    "DB_HOST=staging-db.internal\n"
    "DB_PORT=5432\n"
    "DB_USER=stageuser\n"
    "DB_PASS=stagepass123\n"
    "API_KEY=STG-584af\n"
    "LOG_LEVEL=info\n"
)

EXPECTED_PRD_ENV = (
    "DB_HOST=prod-db.internal\n"
    "DB_PORT=5432\n"
    "DB_USER=produser\n"
    "DB_PASS=prodpass123\n"
    "API_KEY=PRD-9f3cd\n"
    "LOG_LEVEL=warning\n"
)

EXPECTED_CSV = (
    "ENV,KEY,VALUE\n"
    "development,DB_HOST,localhost\n"
    "development,DB_PORT,5432\n"
    "development,DB_USER,devuser\n"
    "development,DB_PASS,devpass123\n"
    "development,API_KEY,DEV-23ab9\n"
    "development,LOG_LEVEL,debug\n"
    "staging,DB_HOST,staging-db.internal\n"
    "staging,DB_PORT,5432\n"
    "staging,DB_USER,stageuser\n"
    "staging,DB_PASS,stagepass123\n"
    "staging,API_KEY,STG-584af\n"
    "staging,LOG_LEVEL,info\n"
    "production,DB_HOST,prod-db.internal\n"
    "production,DB_PORT,5432\n"
    "production,DB_USER,produser\n"
    "production,DB_PASS,prodpass123\n"
    "production,API_KEY,PRD-9f3cd\n"
    "production,LOG_LEVEL,warning\n"
)

EXPECTED_DEPLOY_LOG = (
    "[2023-01-01 00:00:00] ENV=staging export DB_HOST=staging-db.internal\n"
    "[2023-01-01 00:00:00] ENV=staging export DB_PORT=5432\n"
    "[2023-01-01 00:00:00] ENV=staging export API_KEY=STG-584af\n"
    "[2023-01-01 00:00:00] ENV=staging export LOG_LEVEL=info\n"
    "[2023-01-01 00:00:00] ENV=production export DB_HOST=prod-db.internal\n"
    "[2023-01-01 00:00:00] ENV=production export DB_PORT=5432\n"
    "[2023-01-01 00:00:00] ENV=production export API_KEY=PRD-9f3cd\n"
    "[2023-01-01 00:00:00] ENV=production export LOG_LEVEL=warning\n"
)

# ---------- HELPERS -----------------------------------------------------------

def _assert_file(path: Path, expected: str):
    assert path.is_file(), f"Missing file: {path}"
    data = path.read_text(encoding="utf-8")
    assert data == expected, (
        f"Contents of {path} differ from specification.\n"
        "---- expected ----\n"
        f"{expected!r}\n"
        "----   got   ----\n"
        f"{data!r}"
    )
    # Extra safety: ensure file ends with a single UNIX newline
    assert expected.endswith("\n"), "Internal test error: expected strings must end with \\n"
    assert data.endswith("\n"), f"{path} must end with a single UNIX newline"

# ---------- TESTS -------------------------------------------------------------

def test_directory_structure():
    required_dirs = [
        Path("/home/user/releases"),  # pre-existing
        BASE,
        ENV_DIR,
        DEV_DIR,
        STG_DIR,
        PRD_DIR,
    ]
    for d in required_dirs:
        assert d.is_dir(), f"Required directory is missing: {d}"

def test_env_example_file():
    _assert_file(ENV_EXAMPLE, EXPECTED_ENV_EXAMPLE)

@pytest.mark.parametrize(
    "path,expected",
    [
        (DEV_ENV, EXPECTED_DEV_ENV),
        (STG_ENV, EXPECTED_STG_ENV),
        (PRD_ENV, EXPECTED_PRD_ENV),
    ],
)
def test_environment_env_files(path, expected):
    _assert_file(path, expected)

def test_all_envs_summary_csv():
    _assert_file(CSV_FILE, EXPECTED_CSV)
    # Validate line count explicitly
    lines = EXPECTED_CSV.rstrip("\n").split("\n")
    assert len(lines) == 19, "CSV should contain exactly 19 lines"

def test_deploy_vars_log():
    _assert_file(DEPLOY_LOG, EXPECTED_DEPLOY_LOG)
    lines = EXPECTED_DEPLOY_LOG.rstrip("\n").split("\n")
    assert len(lines) == 8, "deploy_vars.log should contain exactly 8 lines"
    # Ensure only whitelisted keys are present
    forbidden_keys = {"DB_USER", "DB_PASS"}
    for line in lines:
        for key in forbidden_keys:
            assert key not in line, f"Forbidden key {key} found in deploy_vars.log"