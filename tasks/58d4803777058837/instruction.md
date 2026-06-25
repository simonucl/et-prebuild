# Git Conditional Profile Repair

Several Git repositories are already staged under `/home/user/work`. Repair the user-level Git configuration so repository identity and safety settings come from `/home/user/.gitconfig` plus include files under `/home/user/.config/git`.

Do not use the network. Do not change any repository's branch, remote URL, commits, or files. Remove stale local profile overrides from repository `.git/config` files instead of relying on them.

Create these include files:

- `/home/user/.config/git/clienta.inc`
- `/home/user/.config/git/security.inc`
- `/home/user/.config/git/release.inc`
- `/home/user/.config/git/hotfix.inc`

Routing rules:

- Repositories under `/home/user/work/clientA/` use the ClientA profile.
- Repositories whose remote URL matches `*://*git.corp.example*/security/**` use the Security profile.
- ClientA repositories on branches matching `release/**` also use the Release profile.
- ClientA repositories on branches matching `hotfix/**` also use the Hotfix profile.
- Personal repositories on `hotfix/**` branches must not receive the Hotfix profile unless they are also under `/home/user/work/clientA/`.

Required effective settings:

| Repository | Branch | Profiles |
| --- | --- | --- |
| `/home/user/work/clientA/service` | `release/1.8` | `clienta`, `release` |
| `/home/user/work/clientA/security/gateway` | `hotfix/CVE-2026-4242` | `clienta`, `security`, `hotfix` |
| `/home/user/work/vendor/security-mirror` | `main` | `default`, `security` |
| `/home/user/work/personal/notes` | `hotfix/private` | `default` |

Default profile:

- `user.name=Jordan Lee`
- `user.email=jordan@personal.example`
- `pull.ff=only`
- no effective `core.sshCommand`, `gpg.format`, `user.signingKey`, `commit.gpgSign`, `tag.gpgSign`, `commit.template`, `commit.cleanup`, `receive.fsckObjects`, `transfer.fsckObjects`, or `push.followTags`

ClientA profile:

- `user.name=Jordan Lee`
- `user.email=jordan.lee@clienta.example`
- `core.sshCommand=ssh -i ~/.ssh/clienta_ed25519 -F /dev/null`
- `gpg.format=ssh`
- `user.signingKey=/home/user/.ssh/clienta_signing.pub`
- `commit.gpgSign=true`

Security profile:

- `user.email=jordan.security@clienta.example`
- `core.sshCommand=ssh -i ~/.ssh/security_ed25519 -F /dev/null`
- `receive.fsckObjects=true`
- `transfer.fsckObjects=true`

Release profile:

- `tag.gpgSign=true`
- `commit.cleanup=scissors`
- `push.followTags=true`

Hotfix profile:

- `commit.template=/home/user/.config/git/hotfix-template.txt`
- `commit.cleanup=scissors`

Also write `/home/user/git_profile_report.json` as one minified JSON line with exactly one trailing newline. Its top-level keys must be `default`, `includes`, and `repositories`, in that order. Summarize the effective values for the four repositories using the profile names and paths above.
