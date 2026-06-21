# test_initial_state.py
#
# Pytest suite that validates the operating-system / filesystem *before*
# the student performs any follow-up actions.  All paths are hard-coded as
# required by the specification—do not change them.

import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

# ---------- Constant paths (must remain literal) ----------
HOME = Path("/home/user")
DEV_DIR = HOME / "dev"

VENV_DIR           = DEV_DIR / ".venv_tools"
VENV_PYTHON        = VENV_DIR / "bin" / "python"          # POSIX location
VENV_BIN_DIR       = VENV_DIR / "bin"                     # used for existence check
VENV_CFG           = VENV_DIR / "pyvenv.cfg"

TOOLS_DIR          = DEV_DIR / "tools"
COMPRESS_SCRIPT    = TOOLS_DIR / "compress.py"

INPUT_FILE         = DEV_DIR / "testdata.txt"
OUTPUT_DIR         = DEV_DIR / "output"
ZIP_FILE           = OUTPUT_DIR / "testdata.zip"

SETUP_LOG          = DEV_DIR / "setup.log"

# Expected artefacts / contents
EXPECTED_LOG_CONTENT = (
    "VENV_SETUP: OK\n"
    "PACKAGE_TQDM: OK\n"
    "ZIP_CREATED: OK\n"
)
EXPECTED_TQDM_VERSION = "4.66.4"
EXPECTED_ZIP_INTERNAL_FILE = "testdata.txt"
EXPECTED_ZIP_INTERNAL_CONTENT = "Lorem ipsum dolor sit amet.\n"

# ------------- Helper functions ---------------------------

def _run(cmd, **kwargs):
    """Run *cmd* (list) and return completed process (raises on failure)."""
    return subprocess.run(
        cmd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        **kwargs,
    )

def _pip_list_json():
    """Return pip list as JSON (list of dicts) using venv's python."""
    try:
        proc = _run([str(VENV_PYTHON), "-m", "pip", "list", "--format=json"])
        return json.loads(proc.stdout)
    except subprocess.CalledProcessError as e:  # pragma: no cover
        pytest.fail(f"Failed to invoke pip list inside virtualenv: {e.stderr}")
    except json.JSONDecodeError as e:  # pragma: no cover
        pytest.fail(f"Could not parse JSON output from pip list: {e}")

# -------------- Tests -------------------------------------

def test_project_directories_and_files_present():
    """Basic presence checks for all required paths."""
    assert DEV_DIR.is_dir(), f"Project directory missing: {DEV_DIR}"
    assert VENV_DIR.is_dir(), f"Virtual-environment directory missing: {VENV_DIR}"
    assert VENV_BIN_DIR.is_dir(), f"Virtual-env 'bin' directory missing: {VENV_BIN_DIR}"
    assert VENV_CFG.is_file(),   f"pyvenv.cfg missing in venv: {VENV_CFG}"

    assert TOOLS_DIR.is_dir(),  f"Tools directory missing: {TOOLS_DIR}"
    assert COMPRESS_SCRIPT.is_file(), f"compress.py missing: {COMPRESS_SCRIPT}"

    assert INPUT_FILE.is_file(), f"Sample input file missing: {INPUT_FILE}"
    assert OUTPUT_DIR.is_dir(),  f"Output directory missing: {OUTPUT_DIR}"
    assert ZIP_FILE.is_file(),   f"Expected zip file missing: {ZIP_FILE}"

    assert SETUP_LOG.is_file(),  f"setup.log missing: {SETUP_LOG}"


def test_virtualenv_python_works_and_imports_tqdm():
    """Ensure the venv's interpreter is functional and can import tqdm."""
    assert VENV_PYTHON.is_file(), f"Python interpreter missing in venv: {VENV_PYTHON}"

    # Verify interpreter reports itself as part of the correct venv
    code = "import sys, os, json; print(json.dumps({'prefix': sys.prefix}))"
    proc = _run([str(VENV_PYTHON), "-c", code])
    data = json.loads(proc.stdout.strip())
    assert Path(data["prefix"]) == VENV_DIR, (
        "The python executable does not belong to the expected virtual environment"
    )

    # Import tqdm and check version
    code = (
        "import json, importlib.metadata, sys;"
        "print(json.dumps({'version': importlib.metadata.version('tqdm')}))"
    )
    proc = _run([str(VENV_PYTHON), "-c", code])
    version = json.loads(proc.stdout.strip())["version"]
    assert version == EXPECTED_TQDM_VERSION, (
        f"tqdm version mismatch inside venv: expected {EXPECTED_TQDM_VERSION}, got {version}"
    )


def test_only_tqdm_present_as_third_party():
    """Check that no extra third-party packages besides tqdm are installed."""
    pkg_list = _pip_list_json()
    # Built-ins that are allowed by spec
    allowed_builtin = {"pip", "setuptools", "wheel"}
    third_party = {pkg["name"] for pkg in pkg_list if pkg["name"] not in allowed_builtin}

    assert third_party == {"tqdm"}, (
        "Unexpected third-party packages installed inside venv: "
        f"{third_party - {'tqdm'}}"
    )

    tqdm_info = next(p for p in pkg_list if p["name"] == "tqdm")
    assert tqdm_info["version"] == EXPECTED_TQDM_VERSION, (
        f"tqdm version mismatch: expected {EXPECTED_TQDM_VERSION}, "
        f"found {tqdm_info['version']}"
    )


def test_sample_input_file_content():
    """Ensure sample input file has exact content."""
    with INPUT_FILE.open("r", encoding="utf-8") as f:
        data = f.read()
    assert data == EXPECTED_ZIP_INTERNAL_CONTENT, (
        "Content of testdata.txt does not match expectation"
    )


def test_zip_has_correct_member_and_content():
    """Verify the zip file contains only the expected member with proper content."""
    assert zipfile.is_zipfile(ZIP_FILE), f"{ZIP_FILE} is not a valid zip archive"

    with zipfile.ZipFile(ZIP_FILE) as zf:
        members = zf.namelist()
        assert members == [EXPECTED_ZIP_INTERNAL_FILE], (
            f"Zip archive should contain exactly one member named "
            f"'{EXPECTED_ZIP_INTERNAL_FILE}', found: {members}"
        )
        with zf.open(EXPECTED_ZIP_INTERNAL_FILE) as f:
            content = f.read().decode("utf-8")
        assert content == EXPECTED_ZIP_INTERNAL_CONTENT, (
            "Content inside zip member does not match expected text"
        )


def test_setup_log_exact_content():
    """setup.log must match the specification byte-for-byte."""
    raw = SETUP_LOG.read_bytes()
    expected = EXPECTED_LOG_CONTENT.encode("ascii")
    assert raw == expected, (
        f"setup.log content mismatch.\nExpected:\n{EXPECTED_LOG_CONTENT!r}\n"
        f"Found:\n{raw.decode('ascii', errors='replace')!r}"
    )


def test_compress_script_can_be_invoked():
    """
    Run compress.py again to ensure it executes correctly.

    We run it with the same input/output; the script should overwrite the zip and
    print a final line "Finished: <abs_path>".
    """
    if not os.access(COMPRESS_SCRIPT, os.X_OK):
        # Even if not executable by flag, `python` should still run it.
        pass

    cmd = [
        str(VENV_PYTHON),
        str(COMPRESS_SCRIPT),
        str(INPUT_FILE),
        str(ZIP_FILE),
    ]
    proc = _run(cmd)

    # The last non-empty line of stdout should be the Finished: <path> message.
    last_line = [ln for ln in proc.stdout.splitlines() if ln.strip()][-1]
    expected_line = f"Finished: {ZIP_FILE}"
    assert last_line == expected_line, (
        "compress.py did not emit the expected completion line.\n"
        f"Expected: {expected_line!r}\nGot: {last_line!r}"
    )

    # Finally, re-validate the zip after overwrite.
    test_zip_has_correct_member_and_content()