FROM ubuntu:22.04

# Author: container-builder
# Description: Apptainer image for semantic-version bump task with initial repo state and pytest installed.

ENV PYTHONUNBUFFERED=1

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN REPO_DIR="/home/user/projects/infra-scripts" && \
    mkdir -p "${REPO_DIR}/terraform" && \
    mkdir -p "${REPO_DIR}/logs" && \
    printf "2.4.7\n" > "${REPO_DIR}/VERSION"

RUN REPO_DIR="/home/user/projects/infra-scripts" && \
    cat <<'EOF' > "${REPO_DIR}/terraform/main.tf"
module "network" {
  source = "git::https://example.com/network.git?ref=v2.4.7"
}

module "monitoring" {
  source = "git::ssh://git@example.com/monitoring.git//modules/agent?ref=v2.4.7"
}
EOF

RUN REPO_DIR="/home/user/projects/infra-scripts" && \
    cat <<'EOF' > "${REPO_DIR}/CHANGELOG.md"
# Changelog
All notable changes to this project will be documented in this file.

## [2.4.7] - 2023-06-02
### Added
- Initial release of production blue/green deployment pipeline.
EOF

RUN REPO_DIR="/home/user/projects/infra-scripts" && \
    chmod 777 "${REPO_DIR}/logs" && \
    chmod -R go+rwX "${REPO_DIR}"

RUN mkdir -p /home/user && chmod 755 /home/user

CMD ["/bin/bash"]