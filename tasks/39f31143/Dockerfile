# Converted from Apptainer: Using ubuntu:22.04 as base, since Docker cannot use a local .sif image
FROM ubuntu:22.04

# ---------------------------------------------------------
# %post commands
# ---------------------------------------------------------
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        tar \
        gzip \
        acl

RUN pip3 install --no-cache-dir pytest

# Create user 'user' with home directory /home/user
RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -s /bin/bash user; \
    fi && \
    chmod 0755 /home/user

# Prepare legacy release tarball
RUN OLD_RELEASES_DIR="/home/user/old_releases" && \
    mkdir -p "${OLD_RELEASES_DIR}" && \
    chmod 0755 "${OLD_RELEASES_DIR}" && \
    WORKDIR="/tmp/release_v1_build" && \
    mkdir -p "${WORKDIR}/release_v1/bin" "${WORKDIR}/release_v1/src" && \
    printf 'Legacy License\n' > "${WORKDIR}/release_v1/LICENSE" && \
    printf '# Release v1\n' > "${WORKDIR}/release_v1/README.md" && \
    printf '#!/bin/sh\necho ok\n' > "${WORKDIR}/release_v1/bin/run.sh" && \
    printf 'int main(){return 0;}\n' > "${WORKDIR}/release_v1/src/main.c" && \
    find "${WORKDIR}/release_v1" -type d -exec chmod 0755 {} + && \
    find "${WORKDIR}/release_v1" -type f -exec chmod 0644 {} + && \
    TAR_PATH="${OLD_RELEASES_DIR}/release_v1.tar.gz" && \
    tar -C "${WORKDIR}" -czf "${TAR_PATH}" release_v1 && \
    chmod 0644 "${TAR_PATH}" && \
    rm -rf "${WORKDIR}"

# Ensure build_logs does not exist
RUN if [ -d /home/user/build_logs ]; then rm -rf /home/user/build_logs; fi

# ---------------------------------------------------------
# %environment
# ---------------------------------------------------------
ENV PATH="$PATH:/usr/local/bin"

# ---------------------------------------------------------
# %runscript
# ---------------------------------------------------------
CMD ["/bin/bash", "-c", "exec \"$@\"", "--"]

# ---------------------------------------------------------
# %labels
# ---------------------------------------------------------
LABEL Author="AI-Apptainer-Builder"
LABEL Description="Environment pre-loaded with a legacy release tarball for QA sanity-check tasks."