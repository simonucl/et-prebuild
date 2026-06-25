import argparse
import importlib.resources
import json

from . import __version__


def main() -> None:
    parser = argparse.ArgumentParser(prog="field-reporter")
    parser.add_argument("--sensor", required=True)
    parser.add_argument("--value", required=True, type=int)
    args = parser.parse_args()

    profile = json.loads(
        importlib.resources.files("field_reporter")
        .joinpath("data/profile.json")
        .read_text(encoding="utf-8")
    )
    payload = {
        "sensor": args.sensor,
        "value": args.value,
        "profile": profile["profile"],
        "unit": profile["unit"],
        "version": __version__,
    }
    print(json.dumps(payload, separators=(",", ":")))
