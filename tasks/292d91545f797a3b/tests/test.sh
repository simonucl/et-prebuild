#!/bin/bash
set -u

mkdir -p /logs/verifier
reward=0
export HOME=/home/user

if python3 - <<'PY'
import json
import os
import subprocess
import sys
from pathlib import Path

os.environ["HOME"] = "/home/user"

KEYS = [
    "user.name",
    "user.email",
    "core.sshCommand",
    "gpg.format",
    "user.signingKey",
    "commit.gpgSign",
    "tag.gpgSign",
    "commit.cleanup",
    "commit.template",
    "core.hooksPath",
    "transfer.fsckObjects",
    "fetch.fsckObjects",
    "push.default",
    "advice.detachedHead",
]

REPOS = [
    {
        "path": "/home/user/work/research/model",
        "branch": "review/quantize",
        "remote": {"origin": "ssh://git.internal.example/research/model.git"},
        "profiles": ["research", "review"],
        "values": {
            "user.name": "Riley Chen",
            "user.email": "riley.research@example.invalid",
            "core.sshCommand": "ssh -i /home/user/.ssh/research_ro -F /dev/null",
            "gpg.format": "ssh",
            "user.signingKey": "/home/user/.ssh/research_signing.pub",
            "commit.gpgSign": "true",
            "tag.gpgSign": "true",
            "commit.cleanup": "scissors",
            "commit.template": None,
            "core.hooksPath": None,
            "transfer.fsckObjects": None,
            "fetch.fsckObjects": None,
            "push.default": "current",
            "advice.detachedHead": "false",
        },
    },
    {
        "path": "/home/user/work/Research/infra",
        "branch": "master",
        "remote": {"origin": "ssh://git.internal.example/platform/infra.git"},
        "profiles": ["research"],
        "values": {
            "user.name": "Riley Chen",
            "user.email": "riley.research@example.invalid",
            "core.sshCommand": "ssh -i /home/user/.ssh/research_ro -F /dev/null",
            "gpg.format": "ssh",
            "user.signingKey": "/home/user/.ssh/research_signing.pub",
            "commit.gpgSign": "true",
            "tag.gpgSign": None,
            "commit.cleanup": None,
            "commit.template": None,
            "core.hooksPath": None,
            "transfer.fsckObjects": None,
            "fetch.fsckObjects": None,
            "push.default": "current",
            "advice.detachedHead": None,
        },
    },
    {
        "path": "/home/user/work/research/security-lib",
        "branch": "review/security-fix",
        "remote": {"origin": "ssh://git.internal.example/security/security-lib.git"},
        "profiles": ["research", "security", "review"],
        "values": {
            "user.name": "Riley Chen",
            "user.email": "riley.security@example.invalid",
            "core.sshCommand": "ssh -i /home/user/.ssh/research_ro -F /dev/null",
            "gpg.format": "ssh",
            "user.signingKey": "/home/user/.ssh/research_signing.pub",
            "commit.gpgSign": "true",
            "tag.gpgSign": "true",
            "commit.cleanup": "scissors",
            "commit.template": "/home/user/.config/git/security-template.txt",
            "core.hooksPath": "/home/user/.config/git/security-hooks",
            "transfer.fsckObjects": "true",
            "fetch.fsckObjects": "true",
            "push.default": "current",
            "advice.detachedHead": "false",
        },
    },
    {
        "path": "/home/user/work/external/vendor-audit",
        "branch": "master",
        "remote": {
            "origin": "https://github.com/vendor/audit.git",
            "security": "ssh://git.internal.example/security/vendor-audit.git",
        },
        "profiles": ["default", "security"],
        "values": {
            "user.name": "Riley Chen",
            "user.email": "riley.security@example.invalid",
            "core.sshCommand": None,
            "gpg.format": None,
            "user.signingKey": None,
            "commit.gpgSign": None,
            "tag.gpgSign": None,
            "commit.cleanup": None,
            "commit.template": "/home/user/.config/git/security-template.txt",
            "core.hooksPath": "/home/user/.config/git/security-hooks",
            "transfer.fsckObjects": "true",
            "fetch.fsckObjects": "true",
            "push.default": None,
            "advice.detachedHead": None,
        },
    },
    {
        "path": "/home/user/work/personal/review-notes",
        "branch": "review/private",
        "remote": {"origin": "https://git.personal.example/riley/review-notes.git"},
        "profiles": ["default"],
        "values": {
            "user.name": "Riley Chen",
            "user.email": "riley@personal.example",
            "core.sshCommand": None,
            "gpg.format": None,
            "user.signingKey": None,
            "commit.gpgSign": None,
            "tag.gpgSign": None,
            "commit.cleanup": None,
            "commit.template": None,
            "core.hooksPath": None,
            "transfer.fsckObjects": None,
            "fetch.fsckObjects": None,
            "push.default": None,
            "advice.detachedHead": None,
        },
    },
]

EXPECTED_REPORT = {
    "default": {"user.name": "Riley Chen", "user.email": "riley@personal.example"},
    "includes": [
        {"name": "research", "path": "/home/user/.config/git/research.inc"},
        {"name": "security", "path": "/home/user/.config/git/security.inc"},
        {"name": "review", "path": "/home/user/.config/git/review.inc"},
    ],
    "repositories": [
        {
            "path": repo["path"],
            "branch": repo["branch"],
            "profiles": repo["profiles"],
            **repo["values"],
        }
        for repo in REPOS
    ],
}

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def git(args, missing_ok=False):
    proc = subprocess.run(["git", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if missing_ok and proc.returncode == 1:
        return None
    if proc.returncode != 0:
        fail(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.rstrip("\n")

def git_repo(repo, args, missing_ok=False):
    return git(["-C", repo, *args], missing_ok=missing_ok)

for path in [
    "/home/user/.gitconfig",
    "/home/user/.config/git/research.inc",
    "/home/user/.config/git/security.inc",
    "/home/user/.config/git/review.inc",
    "/home/user/.config/git/security-template.txt",
    "/home/user/.config/git/security-hooks/pre-commit",
    "/home/user/.ssh/research_ro",
    "/home/user/.ssh/research_signing.pub",
]:
    if not Path(path).exists():
        fail(f"required file is missing: {path}")

include_output = git(["config", "--global", "--get-regexp", r"^includeIf\..*\.path$"])
accepted_global = [
    [
        "includeif.gitdir/i:~/work/research/**.path /home/user/.config/git/research.inc",
        "includeif.gitdir/i:~/work/research/**.path ~/.config/git/research.inc",
    ],
    [
        "includeif.hasconfig:remote.*.url:ssh://git.internal.example/security/**.path /home/user/.config/git/security.inc",
        "includeif.hasconfig:remote.*.url:ssh://git.internal.example/security/**.path ~/.config/git/security.inc",
    ],
]
for options in accepted_global:
    if not any(option in include_output for option in options):
        fail(f"missing or incorrect global conditional include; accepted forms: {options}")

research_includes = git(["config", "--file", "/home/user/.config/git/research.inc", "--get-regexp", r"^includeIf\..*\.path$"])
if "includeif.onbranch:review/**.path /home/user/.config/git/review.inc" not in research_includes:
    fail("review profile must be included from research.inc with onbranch:review/**")

for repo in REPOS:
    repo_path = repo["path"]
    if not (Path(repo_path) / ".git" / "config").is_file():
        fail(f"{repo_path} is no longer a Git repository")
    if git_repo(repo_path, ["branch", "--show-current"]) != repo["branch"]:
        fail(f"{repo_path} is not on branch {repo['branch']}")
    for name, remote in repo["remote"].items():
        if git_repo(repo_path, ["config", "--local", "--get", f"remote.{name}.url"]) != remote:
            fail(f"{repo_path} remote {name} was changed")
    forbidden = git_repo(
        repo_path,
        ["config", "--local", "--get-regexp", r"^(user\.|core\.sshcommand$|core\.hookspath$|gpg\.|commit\.|tag\.|transfer\.|fetch\.fsckobjects$|push\.|advice\.)"],
        missing_ok=True,
    )
    if forbidden:
        fail(f"{repo_path} contains forbidden local profile settings: {forbidden}")
    for key in KEYS:
        expected = repo["values"][key]
        actual = git_repo(repo_path, ["config", "--includes", "--get", key], missing_ok=True)
        if actual != expected:
            fail(f"{repo_path} expected {key}={expected!r}, got {actual!r}")

report_path = Path("/home/user/git-review-routing.json")
if not report_path.is_file():
    fail("git-review-routing.json is missing")
raw = report_path.read_bytes()
if not raw.endswith(b"\n") or raw.count(b"\n") != 1:
    fail("report must be one minified JSON line with exactly one trailing newline")
if b": " in raw or b", " in raw:
    fail("report must be minified without spaces after JSON separators")
try:
    report = json.loads(raw)
except json.JSONDecodeError as exc:
    fail(f"report is not valid JSON: {exc}")
if list(report.keys()) != ["default", "includes", "repositories"]:
    fail("report top-level keys are missing or in the wrong order")
if report != EXPECTED_REPORT:
    fail("report content does not match the required effective routing summary")

print("git conditional routing validated")
PY
then
  reward=1
fi

echo "$reward" > /logs/verifier/reward.txt
exit 0
