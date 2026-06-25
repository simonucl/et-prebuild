from pathlib import Path
import os
import shutil

root = Path("/home/user/release_lab")
if root.exists():
    shutil.rmtree(root)

source = root / "source"
(source / "src" / "rivermark" / "data").mkdir(parents=True)
(source / "src" / "rivermark" / "__pycache__").mkdir(parents=True)
(source / "docs").mkdir()
(source / "tmp").mkdir()
(root / "handoff").mkdir(parents=True)

files = {
    "README.md": "# Rivermark\n\nOffline river gauge formatter used by the field telemetry team.\n",
    "LICENSE": "Copyright 2026 Rivermark Authors\n\nSPDX-License-Identifier: Apache-2.0\n",
    "pyproject.toml": (
        "[project]\n"
        "name = \"rivermark\"\n"
        "version = \"1.2.0\"\n"
        "description = \"Offline river gauge formatter\"\n"
        "requires-python = \">=3.10\"\n"
    ),
    "docs/usage.md": (
        "# Usage\n\n"
        "Run `rivermark --input readings.jsonl` to emit normalized gauge rows.\n"
    ),
    "docs/DRAFT.md": "Internal draft notes. This file is not part of a release.\n",
    "src/rivermark/__init__.py": "__version__ = \"1.2.0\"\n",
    "src/rivermark/cli.py": (
        "import json\n"
        "import sys\n\n"
        "def normalize(row):\n"
        "    return {\"station\": row[\"station\"].upper(), \"level_cm\": int(row[\"level_cm\"])}\n\n"
        "def main(argv=None):\n"
        "    argv = list(sys.argv[1:] if argv is None else argv)\n"
        "    if argv[:1] != [\"--input\"] or len(argv) != 2:\n"
        "        raise SystemExit(\"usage: rivermark --input readings.jsonl\")\n"
        "    with open(argv[1], \"r\", encoding=\"utf-8\") as fh:\n"
        "        for line in fh:\n"
        "            print(json.dumps(normalize(json.loads(line)), separators=(\",\", \":\")))\n\n"
        "if __name__ == \"__main__\":\n"
        "    main()\n"
    ),
    "src/rivermark/data/schema.json": (
        "{\"type\":\"object\",\"required\":[\"station\",\"level_cm\"],"
        "\"properties\":{\"station\":{\"type\":\"string\"},\"level_cm\":{\"type\":\"integer\"}}}\n"
    ),
    "src/rivermark/__pycache__/cli.cpython-312.pyc": "stale bytecode placeholder\n",
    "tmp/build.log": "debug build output that must not be released\n",
    ".gitignore": "__pycache__/\n*.pyc\ntmp/\n",
}

for rel, content in files.items():
    path = source / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")

for path in source.rglob("*"):
    if path.is_dir():
        os.chmod(path, 0o755)
    else:
        os.chmod(path, 0o644)

(root / "handoff" / "rivermark-1.2.0.tar.gz").write_text("stale archive\n", encoding="utf-8")
(root / "handoff" / "manifest.json").write_text("{}\n", encoding="utf-8")
(root / "handoff" / "old-checksums.txt").write_text("stale\n", encoding="utf-8")

for path in root.rglob("*"):
    os.chown(path, 1000, 1000)
os.chown(root, 1000, 1000)
