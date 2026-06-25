FROM ubuntu:24.04

WORKDIR /home/user

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        bash \
        git \
        openssh-client \
        python3 && \
    rm -rf /var/lib/apt/lists/*

RUN set -eux; \
    mkdir -p /home/user/work/clientA/service \
             /home/user/work/clientA/security/gateway \
             /home/user/work/vendor/security-mirror \
             /home/user/work/personal/notes \
             /home/user/.ssh \
             /home/user/.config/git; \
    for repo in \
        /home/user/work/clientA/service \
        /home/user/work/clientA/security/gateway \
        /home/user/work/vendor/security-mirror \
        /home/user/work/personal/notes; do \
      git -C "$repo" init -q; \
      printf 'seed repository for %s\n' "$repo" > "$repo/README.md"; \
      git -C "$repo" add README.md; \
      git -C "$repo" -c user.name='Bootstrap' -c user.email='bootstrap@example.invalid' commit -q -m 'initial import'; \
    done; \
    git -C /home/user/work/clientA/service remote add origin https://git.corp.example/clientA/service.git; \
    git -C /home/user/work/clientA/security/gateway remote add origin ssh://git@git.corp.example:2222/security/gateway.git; \
    git -C /home/user/work/vendor/security-mirror remote add origin https://git.corp.example/security/mirror.git; \
    git -C /home/user/work/personal/notes remote add origin https://git.personal.example/jordan/notes.git; \
    git -C /home/user/work/clientA/service checkout -q -b release/1.8; \
    git -C /home/user/work/clientA/security/gateway checkout -q -b hotfix/CVE-2026-4242; \
    git -C /home/user/work/vendor/security-mirror checkout -q -b main; \
    git -C /home/user/work/personal/notes checkout -q -b hotfix/private; \
    git -C /home/user/work/clientA/service config --local user.email local-service@example.invalid; \
    git -C /home/user/work/clientA/service config --local commit.gpgSign false; \
    git -C /home/user/work/clientA/security/gateway config --local core.sshCommand 'ssh -i ~/.ssh/old_security_key'; \
    git -C /home/user/work/vendor/security-mirror config --local user.name 'Mirror Bot'; \
    printf 'placeholder clientA private key\n' > /home/user/.ssh/clienta_ed25519; \
    printf 'placeholder security private key\n' > /home/user/.ssh/security_ed25519; \
    printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIClientASigningKeyExample jordan@clienta\n' > /home/user/.ssh/clienta_signing.pub; \
    printf '# Hotfix commit\n\nIncident: \nRisk: \nRollback: \n' > /home/user/.config/git/hotfix-template.txt; \
    printf '%s\n' \
      '[user]' \
      '	name = Wrong Default' \
      '	email = wrong@example.invalid' \
      '[includeIf "gitdir:~/work/clientA"]' \
      '	path = ~/.config/git/clienta.inc' \
      > /home/user/.gitconfig; \
    chmod 700 /home/user/.ssh; \
    chmod 600 /home/user/.ssh/clienta_ed25519 /home/user/.ssh/security_ed25519; \
    chmod 644 /home/user/.ssh/clienta_signing.pub /home/user/.config/git/hotfix-template.txt /home/user/.gitconfig; \
    chmod -R u+rwX,go+rX /home/user

ENV HOME=/home/user
CMD ["bash"]
