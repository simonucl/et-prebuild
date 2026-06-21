# test_initial_state.py
#
# This pytest suite validates the initial filesystem state that must be
# present *before* the student creates any new files (script, CSV, …).
#
# It intentionally does NOT look for any output artefacts such as
# /home/user/mobile_ci/tools/generate_build_report.sh or
# /home/user/mobile_ci/reports/build_report.csv – those will be created later
# by the student’s solution.

import os
import glob
import stat
import pytest

HOME = "/home/user"
BASE_DIR = os.path.join(HOME, "mobile_ci")

EXPECTED_DIRS = [
    BASE_DIR,
    os.path.join(BASE_DIR, "builds"),
    os.path.join(BASE_DIR, "builds", "android"),
    os.path.join(BASE_DIR, "builds", "ios"),
    os.path.join(BASE_DIR, "tools"),
    os.path.join(BASE_DIR, "reports"),
]

EXPECTED_APK_FILES = [
    os.path.join(BASE_DIR, "builds", "android", f"app-release_{v}.apk")
    for v in ("1.2.1", "1.2.2", "1.2.3")
]

EXPECTED_IPA_FILES = [
    os.path.join(BASE_DIR, "builds", "ios", f"app-release_{v}.ipa")
    for v in ("1.2.1", "1.2.2", "1.2.3", "1.2.5")
]


@pytest.mark.parametrize("path", EXPECTED_DIRS)
def test_required_directories_exist(path):
    assert os.path.isdir(path), f"Required directory missing: {path}"


def _is_mode(path, mode_bits):
    """Return True if all mode_bits are set for the path."""
    return os.stat(path).st_mode & mode_bits == mode_bits


@pytest.mark.parametrize("path", EXPECTED_DIRS)
def test_required_directories_are_executable(path):
    # Directories must be traversable (execute bit set).
    exec_bits = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
    assert _is_mode(path, exec_bits), f"Directory not traversable: {path}"


@pytest.mark.parametrize("path", EXPECTED_APK_FILES + EXPECTED_IPA_FILES)
def test_placeholder_artifacts_exist(path):
    assert os.path.isfile(path), f"Expected placeholder file missing: {path}"


def test_android_directory_contains_only_expected_apks():
    apk_dir = os.path.join(BASE_DIR, "builds", "android")
    found_apks = sorted(glob.glob(os.path.join(apk_dir, "*.apk")))
    assert found_apks == sorted(EXPECTED_APK_FILES), (
        "Android builds directory should contain exactly the expected APK "
        f"files.\nExpected: {EXPECTED_APK_FILES}\nFound:    {found_apks}"
    )


def test_ios_directory_contains_only_expected_ipas():
    ipa_dir = os.path.join(BASE_DIR, "builds", "ios")
    found_ipas = sorted(glob.glob(os.path.join(ipa_dir, "*.ipa")))
    assert found_ipas == sorted(EXPECTED_IPA_FILES), (
        "iOS builds directory should contain exactly the expected IPA "
        f"files.\nExpected: {EXPECTED_IPA_FILES}\nFound:    {found_ipas}"
    )


def test_reports_directory_is_initially_empty():
    """
    The reports directory must start empty. The student will later create
    build_report.csv there.
    """
    reports_dir = os.path.join(BASE_DIR, "reports")
    entries = [
        name
        for name in os.listdir(reports_dir)
        if not name.startswith(".")  # ignore hidden files like .gitkeep
    ]
    assert not entries, (
        f"/home/user/mobile_ci/reports should be empty initially. "
        f"Unexpected entries found: {entries}"
    )