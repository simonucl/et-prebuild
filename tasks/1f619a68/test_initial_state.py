# test_initial_state.py
#
# Pytest suite that verifies the initial filesystem state
# before the student executes the task described in the prompt.
#
# It checks:
#   • Presence of all required files and directories.
#   • Absence of the archive and log that the student must create.
#   • That *exactly* the expected set of optimisation-model files
#     (.lp and .mps) is present—no more, no fewer, and that their
#     paths are correct and relative to /home/user/opt_project.

import hashlib
from pathlib import Path

import pytest

ROOT = Path("/home/user/opt_project").resolve()

# ---------------------------------------------------------------------------
# Expected filesystem layout
# ---------------------------------------------------------------------------

# Every file that must already exist (absolute paths)
EXPECTED_FILES = {
    ROOT / "README.md",
    ROOT / "setup.py",
    ROOT / "src/solver.py",
    ROOT / "src/models/modelA.lp",
    ROOT / "src/models/modelB.mps",
    ROOT / "data/demand.csv",
    ROOT / "data/scenario.lp",
    ROOT / "tests/test_parser.py",
    ROOT / "legacy/old_model.mps",
}

# Expected directories (absolute paths)
EXPECTED_DIRS = {
    ROOT,
    ROOT / "src",
    ROOT / "src/models",
    ROOT / "data",
    ROOT / "tests",
    ROOT / "legacy",
}

# Expected optimisation model files (paths *relative* to ROOT)
EXPECTED_MODEL_REL_PATHS = {
    Path("src/models/modelA.lp"),
    Path("src/models/modelB.mps"),
    Path("data/scenario.lp"),
    Path("legacy/old_model.mps"),
}

# Paths that must *not* exist yet
ARTIFACT_TARBALL = ROOT / "models_bundle.tar.gz"
ARTIFACT_LOGFILE = ROOT / "models_bundle.log"

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def relative_to_root(abs_path: Path) -> Path:
    """Return the path of `abs_path` relative to `ROOT`."""
    return abs_path.relative_to(ROOT)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("dir_path", sorted(EXPECTED_DIRS))
def test_expected_directories_exist(dir_path: Path):
    assert dir_path.is_dir(), f"Expected directory missing: {dir_path}"


@pytest.mark.parametrize("file_path", sorted(EXPECTED_FILES))
def test_expected_files_exist(file_path: Path):
    assert file_path.is_file(), f"Expected file missing: {file_path}"


def test_no_artifacts_exist_yet():
    assert not ARTIFACT_TARBALL.exists(), (
        f"Archive {ARTIFACT_TARBALL} should NOT exist before the task is run."
    )
    assert not ARTIFACT_LOGFILE.exists(), (
        f"Log file {ARTIFACT_LOGFILE} should NOT exist before the task is run."
    )


def test_exact_model_file_set():
    """
    Verify that *exactly* the expected optimisation model files (.lp/.mps)
    are present in the project tree and nothing else.
    """
    # Collect every .lp and .mps file found under ROOT (relative paths)
    discovered_models = {
        relative_to_root(p)
        for p in ROOT.rglob("*")
        if p.is_file() and p.suffix in {".lp", ".mps"}
    }

    missing = EXPECTED_MODEL_REL_PATHS - discovered_models
    extra = discovered_models - EXPECTED_MODEL_REL_PATHS

    assert not missing, (
        "The following optimisation-model file(s) are missing:\n"
        + "\n".join(str(ROOT / m) for m in sorted(missing))
    )

    assert not extra, (
        "Unexpected optimisation-model file(s) found in project tree:\n"
        + "\n".join(str(ROOT / e) for e in sorted(extra))
    )