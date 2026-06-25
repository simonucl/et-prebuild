FROM python:3.12-bookworm

WORKDIR /home/user

RUN set -eux; \
  mkdir -p /home/user/work/research/model \
           /home/user/work/Research/infra \
           /home/user/work/research/security-lib \
           /home/user/work/external/vendor-audit \
           /home/user/work/personal/review-notes \
           /home/user/.config/git/security-hooks \
           /home/user/.ssh; \
  printf 'Security-Review:\n\nRisk:\n' > /home/user/.config/git/security-template.txt; \
  printf '#!/bin/sh\nexit 0\n' > /home/user/.config/git/security-hooks/pre-commit; \
  chmod +x /home/user/.config/git/security-hooks/pre-commit; \
  printf 'placeholder research identity\n' > /home/user/.ssh/research_ro; \
  printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBresearchplaceholder user@host\n' > /home/user/.ssh/research_signing.pub; \
  chmod 600 /home/user/.ssh/research_ro; \
  for repo in \
    /home/user/work/research/model \
    /home/user/work/Research/infra \
    /home/user/work/research/security-lib \
    /home/user/work/external/vendor-audit \
    /home/user/work/personal/review-notes; do \
      git init -q "$repo"; \
      git -C "$repo" config user.name bootstrap; \
      git -C "$repo" config user.email bootstrap@example.invalid; \
      printf '%s\n' "seed for $repo" > "$repo/README.md"; \
      git -C "$repo" add README.md; \
      git -C "$repo" commit -q -m 'seed repository'; \
      git -C "$repo" config --unset user.name; \
      git -C "$repo" config --unset user.email; \
    done; \
  git -C /home/user/work/research/model remote add origin ssh://git.internal.example/research/model.git; \
  git -C /home/user/work/research/model checkout -q -b review/quantize; \
  git -C /home/user/work/Research/infra remote add origin ssh://git.internal.example/platform/infra.git; \
  git -C /home/user/work/research/security-lib remote add origin ssh://git.internal.example/security/security-lib.git; \
  git -C /home/user/work/research/security-lib checkout -q -b review/security-fix; \
  git -C /home/user/work/external/vendor-audit remote add origin https://github.com/vendor/audit.git; \
  git -C /home/user/work/external/vendor-audit remote add security ssh://git.internal.example/security/vendor-audit.git; \
  git -C /home/user/work/personal/review-notes remote add origin https://git.personal.example/riley/review-notes.git; \
  git -C /home/user/work/personal/review-notes checkout -q -b review/private; \
  cat > /home/user/.gitconfig <<'EOF'
[user]
	name = Stale User
	email = stale@example.invalid
[commit]
	gpgSign = false
EOF
ENV HOME=/home/user
