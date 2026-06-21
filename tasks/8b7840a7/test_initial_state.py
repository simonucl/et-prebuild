# test_initial_state.py
#
# This test-suite validates that the filesystem *before* the student begins
# working on the task matches the specification given in the prompt.
#
# It makes no assertions about any build artefacts (dist/, *.bundle.*, etc.)
# or about the build script itself—those belong to the *solution* stage.
#
# Only the Python standard library and pytest are used.

import os
from pathlib import Path

PROJECT_ROOT = Path("/home/user/web_project")

# Source files and their exact one-line contents (each terminates with '\n')
EXPECTED_SOURCES = {
    PROJECT_ROOT / "src/css/style1.css": "body { background: #fff; }\n",
    PROJECT_ROOT / "src/css/style2.css": "h1 { color: #333; }\n",
    PROJECT_ROOT / "src/js/app.js":      "console.log('App loaded');\n",
    PROJECT_ROOT / "src/js/utils.js":    "function sum(a,b){return a+b;}\n",
    PROJECT_ROOT / "src/index.html":     "<!DOCTYPE html><html><head><title>Home</title></head><body><h1>Home</h1></body></html>\n",
    PROJECT_ROOT / "src/about.html":     "<!DOCTYPE html><html><head><title>About</title></head><body><h1>About</h1></body></html>\n",
}


def test_project_root_exists():
    assert PROJECT_ROOT.is_dir(), (
        f"Expected project root {PROJECT_ROOT} to exist and be a directory."
    )


def test_expected_source_files_exist():
    missing = [p for p in EXPECTED_SOURCES if not p.is_file()]
    assert not missing, (
        "The following expected source files are missing:\n" +
        "\n".join(str(p) for p in missing)
    )


def test_expected_source_file_contents():
    bad_contents = []
    for path, expected in EXPECTED_SOURCES.items():
        with path.open("r", encoding="utf-8") as f:
            actual = f.read()
        if actual != expected:
            bad_contents.append(
                f"{path} does not match expected content.\n"
                f"Expected: {repr(expected)}\n"
                f"Actual:   {repr(actual)}"
            )
    assert not bad_contents, "One or more source files have unexpected contents:\n" + "\n\n".join(bad_contents)


def test_no_dist_directory_yet():
    dist = PROJECT_ROOT / "dist"
    assert not dist.exists(), (
        f"The directory {dist} should NOT exist before the build script runs."
    )


def test_no_build_script_yet():
    build_script = PROJECT_ROOT / "build_assets.sh"
    assert not build_script.exists(), (
        f"{build_script} should not exist in the initial state; "
        "the student is expected to create it."
    )