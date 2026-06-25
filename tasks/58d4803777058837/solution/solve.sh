#!/bin/bash
set -euo pipefail

export HOME=/home/user

mkdir -p /home/user/.config/git

cat > /home/user/.gitconfig <<'EOF'
[user]
	name = Jordan Lee
	email = jordan@personal.example
[pull]
	ff = only
[includeIf "gitdir:~/work/clientA/**"]
	path = ~/.config/git/clienta.inc
[includeIf "hasconfig:remote.*.url:*://*git.corp.example*/security/**"]
	path = ~/.config/git/security.inc
EOF

cat > /home/user/.config/git/clienta.inc <<'EOF'
[user]
	name = Jordan Lee
	email = jordan.lee@clienta.example
	signingKey = /home/user/.ssh/clienta_signing.pub
[core]
	sshCommand = ssh -i ~/.ssh/clienta_ed25519 -F /dev/null
[gpg]
	format = ssh
[commit]
	gpgSign = true
[includeIf "onbranch:release/**"]
	path = ~/.config/git/release.inc
[includeIf "onbranch:hotfix/**"]
	path = ~/.config/git/hotfix.inc
EOF

cat > /home/user/.config/git/security.inc <<'EOF'
[user]
	email = jordan.security@clienta.example
[core]
	sshCommand = ssh -i ~/.ssh/security_ed25519 -F /dev/null
[receive]
	fsckObjects = true
[transfer]
	fsckObjects = true
EOF

cat > /home/user/.config/git/release.inc <<'EOF'
[tag]
	gpgSign = true
[commit]
	cleanup = scissors
[push]
	followTags = true
EOF

cat > /home/user/.config/git/hotfix.inc <<'EOF'
[commit]
	template = /home/user/.config/git/hotfix-template.txt
	cleanup = scissors
EOF

for repo in \
  /home/user/work/clientA/service \
  /home/user/work/clientA/security/gateway \
  /home/user/work/vendor/security-mirror \
  /home/user/work/personal/notes; do
  for key in \
    user.name user.email core.sshCommand gpg.format user.signingKey \
    commit.gpgSign tag.gpgSign commit.template commit.cleanup \
    receive.fsckObjects transfer.fsckObjects push.followTags pull.ff; do
    git -C "$repo" config --local --unset-all "$key" 2>/dev/null || true
  done
done

python3 - <<'PY'
import json
from pathlib import Path

report = {
    "default": {
        "user.name": "Jordan Lee",
        "user.email": "jordan@personal.example",
        "pull.ff": "only",
    },
    "includes": [
        {"name": "clienta", "path": "/home/user/.config/git/clienta.inc"},
        {"name": "security", "path": "/home/user/.config/git/security.inc"},
        {"name": "release", "path": "/home/user/.config/git/release.inc"},
        {"name": "hotfix", "path": "/home/user/.config/git/hotfix.inc"},
    ],
    "repositories": [
        {
            "path": "/home/user/work/clientA/service",
            "branch": "release/1.8",
            "profiles": ["clienta", "release"],
            "user.name": "Jordan Lee",
            "user.email": "jordan.lee@clienta.example",
            "pull.ff": "only",
            "core.sshCommand": "ssh -i ~/.ssh/clienta_ed25519 -F /dev/null",
            "gpg.format": "ssh",
            "user.signingKey": "/home/user/.ssh/clienta_signing.pub",
            "commit.gpgSign": "true",
            "tag.gpgSign": "true",
            "commit.template": None,
            "commit.cleanup": "scissors",
            "receive.fsckObjects": None,
            "transfer.fsckObjects": None,
            "push.followTags": "true",
        },
        {
            "path": "/home/user/work/clientA/security/gateway",
            "branch": "hotfix/CVE-2026-4242",
            "profiles": ["clienta", "security", "hotfix"],
            "user.name": "Jordan Lee",
            "user.email": "jordan.security@clienta.example",
            "pull.ff": "only",
            "core.sshCommand": "ssh -i ~/.ssh/security_ed25519 -F /dev/null",
            "gpg.format": "ssh",
            "user.signingKey": "/home/user/.ssh/clienta_signing.pub",
            "commit.gpgSign": "true",
            "tag.gpgSign": None,
            "commit.template": "/home/user/.config/git/hotfix-template.txt",
            "commit.cleanup": "scissors",
            "receive.fsckObjects": "true",
            "transfer.fsckObjects": "true",
            "push.followTags": None,
        },
        {
            "path": "/home/user/work/vendor/security-mirror",
            "branch": "main",
            "profiles": ["default", "security"],
            "user.name": "Jordan Lee",
            "user.email": "jordan.security@clienta.example",
            "pull.ff": "only",
            "core.sshCommand": "ssh -i ~/.ssh/security_ed25519 -F /dev/null",
            "gpg.format": None,
            "user.signingKey": None,
            "commit.gpgSign": None,
            "tag.gpgSign": None,
            "commit.template": None,
            "commit.cleanup": None,
            "receive.fsckObjects": "true",
            "transfer.fsckObjects": "true",
            "push.followTags": None,
        },
        {
            "path": "/home/user/work/personal/notes",
            "branch": "hotfix/private",
            "profiles": ["default"],
            "user.name": "Jordan Lee",
            "user.email": "jordan@personal.example",
            "pull.ff": "only",
            "core.sshCommand": None,
            "gpg.format": None,
            "user.signingKey": None,
            "commit.gpgSign": None,
            "tag.gpgSign": None,
            "commit.template": None,
            "commit.cleanup": None,
            "receive.fsckObjects": None,
            "transfer.fsckObjects": None,
            "push.followTags": None,
        },
    ],
}
Path("/home/user/git_profile_report.json").write_text(
    json.dumps(report, separators=(",", ":")) + "\n",
    encoding="utf-8",
)
PY
