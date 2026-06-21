FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Build Script"
LABEL Description="Minimal environment with a mock Git repository and sub-module for audit-trail task, plus pytest installed."

# ---------- Base packages ----------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata \
        curl && \
    rm -rf /var/lib/apt/lists/*

# ---------- Python tooling ----------
RUN pip3 install --no-cache-dir pytest

# ---------- Directory structure ----------
RUN mkdir -p /home/user/project/libs/json && \
    mkdir -p /home/user/audit && \
    chmod -R 0755 /home/user

# ---------- Git metadata placeholders ----------
# Main repo
RUN mkdir -p /home/user/project/.git && \
    echo "Main project" > /home/user/project/README.md

# .gitmodules registering the submodule
RUN cat > /home/user/project/.gitmodules <<'EOF'
[submodule "libs/json"]
    path = libs/json
    url = https://example.com/json.git
EOF

# Sub-module repo placeholder
RUN mkdir -p /home/user/project/libs/json/.git

# ---------- Mock Git implementation ----------
RUN cat > /usr/local/bin/git <<'EOS'
#!/usr/bin/env bash
set -e

cmd="$1"
shift || true

case "$cmd" in
  status)
      # Expected invocation: git status --short
      if [[ "$1" == "--short" ]]; then
          # Clean working tree ⇒ no output
          exit 0
      fi
      ;;
  submodule)
      # Expected invocation: git submodule status
      if [[ "$1" == "status" ]]; then
          echo " abcd1234567890abcdef1234567890abcdef12 libs/json (heads/master)"
          exit 0
      fi
      ;;
  rev-parse)
      # Expected invocation: git rev-parse HEAD
      if [[ "$1" == "HEAD" ]]; then
          cwd="$(pwd)"
          if [[ "$cwd" == */libs/json* ]]; then
              # We're inside the sub-module
              echo "abcd1234567890abcdef1234567890abcdef12"
          else
              # Top-level repository
              echo "7890abcd1234567890abcdef1234567890abcd"
          fi
          exit 0
      fi
      ;;
esac

echo "git (mock): unsupported command or arguments: $cmd $*" >&2
exit 1
EOS

RUN chmod +x /usr/local/bin/git

# ---------- Environment ----------
ENV PATH="/usr/local/bin:${PATH}"

# Ensure permissions on container start
RUN chmod 755 /home/user