# test_initial_state.py
"""
Pytest suite that validates the initial filesystem state *before* the student
performs any actions for the “ML data-prep” exercise.

Only the pre-existing input sources are tested.  None of the paths the student
is required to create (`/home/user/ml_data_prep/`, the extracted directory,
or the log file) are referenced here, in compliance with the grading rules.
"""
from pathlib import Path
import pytest

HOME = Path("/home/user")
SRC_IMAGES = HOME / "source_images"
SRC_LABELS = HOME / "source_labels"


def _collect_files(directory: Path, suffix: str):
    """
    Helper that returns a list of Path objects in `directory` that end with `suffix`.
    Hidden files and sub-directories are ignored.
    """
    return [
        p for p in directory.iterdir()
        if p.is_file() and p.name.lower().endswith(suffix.lower())
    ]


@pytest.mark.describe("Initial source directories exist with expected files")
class TestInitialSourceState:
    # 1 ──────────────────────────────────────────────────────────────────────
    def test_source_image_dir_exists(self):
        assert SRC_IMAGES.exists(), (
            f"Required directory {SRC_IMAGES} is missing."
        )
        assert SRC_IMAGES.is_dir(), (
            f"{SRC_IMAGES} exists but is not a directory."
        )

    # 2 ──────────────────────────────────────────────────────────────────────
    def test_source_label_dir_exists(self):
        assert SRC_LABELS.exists(), (
            f"Required directory {SRC_LABELS} is missing."
        )
        assert SRC_LABELS.is_dir(), (
            f"{SRC_LABELS} exists but is not a directory."
        )

    # 3 ──────────────────────────────────────────────────────────────────────
    def test_source_images_have_jpg_files(self):
        jpg_files = _collect_files(SRC_IMAGES, ".jpg")
        assert jpg_files, (
            f"No '.jpg' files found in {SRC_IMAGES}; "
            "at least one JPEG file is required."
        )
        # Extra sanity: ensure each file is non-empty.
        empties = [p for p in jpg_files if p.stat().st_size == 0]
        assert not empties, (
            "The following JPEG files are unexpectedly empty: "
            + ", ".join(str(p) for p in empties)
        )

    # 4 ──────────────────────────────────────────────────────────────────────
    def test_source_labels_have_json_files(self):
        json_files = _collect_files(SRC_LABELS, ".json")
        assert json_files, (
            f"No '.json' files found in {SRC_LABELS}; "
            "at least one JSON label file is required."
        )
        empties = [p for p in json_files if p.stat().st_size == 0]
        assert not empties, (
            "The following JSON files are unexpectedly empty: "
            + ", ".join(str(p) for p in empties)
        )

    # 5 ──────────────────────────────────────────────────────────────────────
    def test_no_subdirectories_or_unexpected_files(self):
        """
        Enforce a clean setup: only JPG files in source_images and
        only JSON files in source_labels.  Any sub-directories or other
        file types would indicate an unexpected initial state.
        """
        other_in_images = [
            p for p in SRC_IMAGES.iterdir()
            if p.is_file() and not p.name.lower().endswith(".jpg")
        ] + [p for p in SRC_IMAGES.iterdir() if p.is_dir()]
        assert not other_in_images, (
            f"Unexpected items found in {SRC_IMAGES}: "
            + ", ".join(str(p) for p in other_in_images)
        )

        other_in_labels = [
            p for p in SRC_LABELS.iterdir()
            if p.is_file() and not p.name.lower().endswith(".json")
        ] + [p for p in SRC_LABELS.iterdir() if p.is_dir()]
        assert not other_in_labels, (
            f"Unexpected items found in {SRC_LABELS}: "
            + ", ".join(str(p) for p in other_in_labels)
        )