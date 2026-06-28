# trsi-base — canonical base for terminal-rsi generated environments.
# FROM an MAR (mcr.microsoft.com) image: public + Azure-CDN-backed -> fast anonymous pulls from
# aks-modal (which is on Azure and has no registry-auth knob), and no Docker Hub rate limits.
# Debian-bookworm + python3.12 + dev tooling preinstalled; we add the harbor/terminus-2 agent
# runtime (tmux!) and common terminal-task tools so every env overlay is thin and reproducible.
FROM mcr.microsoft.com/devcontainers/python:dev-3.12-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
      tmux git curl ca-certificates jq build-essential procps less unzip xz-utils \
    && rm -rf /var/lib/apt/lists/*

# fail the build loudly if the harbor agent runtime is missing
RUN tmux -V && git --version && python3 --version && bash -lc 'echo trsi-base ok'

CMD ["bash"]
