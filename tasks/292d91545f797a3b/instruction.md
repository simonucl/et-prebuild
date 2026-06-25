# Repair Git Conditional Review Profiles

Several Git repositories already exist under `/home/user/work`. Repair only the user-level Git configuration under `/home/user/.gitconfig` and include files under `/home/user/.config/git` so Git selects the right effective profile by conditional includes.

Do not edit any repository's local `.git/config` to set identities, signing settings, SSH commands, hooks, templates, cleanup behavior, fsck behavior, push behavior, or advice settings. Preserve the existing repositories, remotes, branches, commits, SSH placeholder files, security hook directory, and security commit template.

Use these include files:

- Research profile: `/home/user/.config/git/research.inc`
- Security profile: `/home/user/.config/git/security.inc`
- Review profile: `/home/user/.config/git/review.inc`

Required routing:

- Repositories under `/home/user/work/research/` must use the research profile, matched case-insensitively. This must also cover the existing uppercase path `/home/user/work/Research/infra`.
- Repositories with any remote URL matching `ssh://git.internal.example/security/**` must use the security profile.
- Research repositories on branches matching `review/**` must use the review profile. Include the review profile from the research profile, not directly from `/home/user/.gitconfig`.
- A non-research repository on a `review/**` branch must not get the review profile.

Default personal profile:

- `user.name=Riley Chen`
- `user.email=riley@personal.example`
- no effective `core.sshCommand`
- no effective `gpg.format`
- no effective `user.signingKey`
- no effective `commit.gpgSign`
- no effective `tag.gpgSign`
- no effective `commit.cleanup`
- no effective `commit.template`
- no effective `core.hooksPath`
- no effective `transfer.fsckObjects`
- no effective `fetch.fsckObjects`
- no effective `push.default`
- no effective `advice.detachedHead`

Research profile:

- `user.email=riley.research@example.invalid`
- `core.sshCommand=ssh -i /home/user/.ssh/research_ro -F /dev/null`
- `gpg.format=ssh`
- `user.signingKey=/home/user/.ssh/research_signing.pub`
- `commit.gpgSign=true`
- `push.default=current`

Security profile:

- `user.email=riley.security@example.invalid`
- `commit.template=/home/user/.config/git/security-template.txt`
- `core.hooksPath=/home/user/.config/git/security-hooks`
- `transfer.fsckObjects=true`
- `fetch.fsckObjects=true`

Review profile:

- `tag.gpgSign=true`
- `commit.cleanup=scissors`
- `advice.detachedHead=false`

Expected repository behavior:

| Repository | Current branch | Profiles |
| --- | --- | --- |
| `/home/user/work/research/model` | `review/quantize` | research plus review |
| `/home/user/work/Research/infra` | `master` | research |
| `/home/user/work/research/security-lib` | `review/security-fix` | research plus security plus review |
| `/home/user/work/external/vendor-audit` | `master` | default plus security |
| `/home/user/work/personal/review-notes` | `review/private` | default only |

Also write `/home/user/git-review-routing.json` as minified JSON with exactly one trailing newline. Its top-level keys must be, in order: `default`, `includes`, `repositories`. Use the actual absolute include-file paths you created.

The report shape must be:

```json
{"default":{"user.name":"Riley Chen","user.email":"riley@personal.example"},"includes":[{"name":"research","path":"<absolute research include path>"},{"name":"security","path":"<absolute security include path>"},{"name":"review","path":"<absolute review include path>"}],"repositories":[{"path":"<repo path>","branch":"<branch>","profiles":["<profile names in order>"],"user.name":"<effective value>","user.email":"<effective value>","core.sshCommand":null,"gpg.format":null,"user.signingKey":null,"commit.gpgSign":null,"tag.gpgSign":null,"commit.cleanup":null,"commit.template":null,"core.hooksPath":null,"transfer.fsckObjects":null,"fetch.fsckObjects":null,"push.default":null,"advice.detachedHead":null}]}
```
