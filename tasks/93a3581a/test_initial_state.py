# test_initial_state.py
#
# This test-suite validates the **initial** state of the filesystem
# *before* the student performs any actions for the “*.tmp → *.bak”
# renaming task.  It intentionally FAILS if anything already looks as
# though work has been done (e.g. a “.bak” file or a log file already
# exists) or if the starting data set is incomplete.

import os
from pathlib import Path

BASE_DIR = Path("/home/user/pipeline_configs").resolve()

# ---------------------------------------------------------------------------
# Helper data describing the expected initial layout
# ---------------------------------------------------------------------------

EXPECTED_DIRS = [
    BASE_DIR,
    BASE_DIR / "app1",
    BASE_DIR / "app2",
]

TMP_FILES_AND_CONTENT = {
    BASE_DIR / "app1" / "staging.conf.tmp":
        "# temporary staging configuration\n",
    BASE_DIR / "app1" / "prod.conf.tmp":
        "# temporary production configuration\n",
    BASE_DIR / "app2" / "dev.conf.tmp":
        "# temporary development configuration\n",
}

UNTOUCHED_FILES_AND_CONTENT = {
    BASE_DIR / "app1" / "settings.conf":
        "# permanent config – do not touch\n",
}

# Files that **must not** exist yet
FORBIDDEN_PATHS = [
    # Corresponding “.bak” files
    *(p.with_suffix(".bak") for p in TMP_FILES_AND_CONTENT),
    # The log file that the batch job is supposed to create
    BASE_DIR / "rename_report.log",
]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_required_directories_exist_and_are_directories():
    """
    Ensure all expected directories exist and are directories.
    """
    missing_dirs = [str(d) for d in EXPECTED_DIRS if not d.is_dir()]
    assert not missing_dirs, (
        "The following required directories are missing "
        f"(or are not directories): {', '.join(missing_dirs)}"
    )


def test_tmp_files_exist_with_expected_contents():
    """
    All *.tmp files must be present *with exact contents* before any action.
    """
    problems = []

    for path, expected_content in TMP_FILES_AND_CONTENT.items():
        if not path.is_file():
            problems.append(f"Missing file: {path}")
            continue

        try:
            data = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            problems.append(f"Cannot read {path}: {exc}")
            continue

        if data != expected_content:
            problems.append(f"Content mismatch in {path!s}")

    assert not problems, (
        "Issues found with required *.tmp files:\n" + "\n".join(problems)
    )


def test_other_files_exist_with_expected_contents():
    """
    Files that must remain untouched (e.g. settings.conf) are present and intact.
    """
    problems = []

    for path, expected_content in UNTOUCHED_FILES_AND_CONTENT.items():
        if not path.is_file():
            problems.append(f"Missing required file: {path}")
            continue

        try:
            data = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            problems.append(f"Cannot read {path}: {exc}")
            continue

        if data != expected_content:
            problems.append(f"Content mismatch in {path!s}")

    assert not problems, (
        "Issues found with files that must remain untouched:\n" + "\n".join(problems)
    )


def test_forbidden_paths_do_not_exist_yet():
    """
    Make sure no *.bak files or the rename_report.log exist *before* the exercise.
    Their presence would indicate that the operation was run prematurely.
    """
    existing = [str(p) for p in FORBIDDEN_PATHS if p.exists()]
    assert not existing, (
        "The following files/directories already exist but should NOT be present "
        "before the renaming task is executed:\n" + "\n".join(existing)
    )


def test_no_extra_tmp_files_present():
    """
    The tree should contain exactly the known *.tmp files and no others.
    This guards against accidental additions that would break evaluation logic.
    """
    found_tmp_files = list(BASE_DIR.rglob("*.tmp"))
    expected_tmp_set = set(TMP_FILES_AND_CONTENT.keys())
    found_tmp_set = set(found_tmp_files)

    extra_tmp_files = found_tmp_set - expected_tmp_set
    missing_tmp_files = expected_tmp_set - found_tmp_set

    problems = []
    if extra_tmp_files:
        problems.append(
            "Unexpected *.tmp files present:\n" +
            "\n".join(str(p) for p in sorted(extra_tmp_files))
        )
    if missing_tmp_files:
        problems.append(
            "Expected *.tmp files missing:\n" +
            "\n".join(str(p) for p in sorted(missing_tmp_files))
        )

    assert not problems, "\n\n".join(problems)