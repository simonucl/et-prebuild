FROM ubuntu:22.04

# Labels
LABEL Author="build-engineering-task"
LABEL Description="Container pre-populated for the \"age-out stale JARs\" exercise."

# Basic tooling
RUN set -eux && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        tzdata && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user that will own the working tree
# (UID 1000 is the conventional first user on Ubuntu)
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -s /bin/bash user; \
    fi

# Build the initial directory layout and files expected by the tests
RUN set -eux && \
    BASE=/home/user/workspace && \
    BUILDS=${BASE}/builds && \
    ARTIFACTS=${BUILDS}/artifacts && \
    ARCHIVE=${BUILDS}/archive && \
    mkdir -p "${ARTIFACTS}" "${ARCHIVE}" && \
    printf 'dummy jar 1.0.0\n' > "${ARTIFACTS}/app-core-1.0.0.jar" && \
    printf 'dummy jar 1.1.0\n' > "${ARTIFACTS}/app-core-1.1.0.jar" && \
    printf 'dummy jar 2.0.0\n' > "${ARTIFACTS}/lib-util-2.0.0.jar" && \
    touch -d '10 days ago' \
        "${ARTIFACTS}/app-core-1.0.0.jar" \
        "${ARTIFACTS}/app-core-1.1.0.jar" \
        "${ARTIFACTS}/lib-util-2.0.0.jar" && \
    printf 'dummy jar latest\n' > "${ARTIFACTS}/fresh-feature-9999.jar" && \
    chmod 0755 "${BASE}" "${BUILDS}" "${ARTIFACTS}" "${ARCHIVE}" && \
    chmod 0644 "${ARTIFACTS}"/*.jar && \
    chown -R 1000:1000 "${BASE}"

# Create README.txt file
RUN cat > /home/user/workspace/builds/artifacts/README.txt <<EOF
Build Drop Area
---------------
Anything that is not a *.jar file
will stay here.
EOF

# Set permissions and timestamps for README and fresh JAR
RUN touch -d '1 hour ago' /home/user/workspace/builds/artifacts/fresh-feature-9999.jar /home/user/workspace/builds/artifacts/README.txt && \
    chmod 0644 /home/user/workspace/builds/artifacts/README.txt && \
    chown 1000:1000 /home/user/workspace/builds/artifacts/README.txt

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

# Default command
CMD ["echo", "This container is meant to be used via 'docker exec ...' with your own commands. It only prepares the initial build-artifact state for the exercise."]