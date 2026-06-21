# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---------------------------------------------------------------------
# Install Python and pytest
# ---------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ---------------------------------------------------------------------
# Create initial workspace under /home/user with required log files
# ---------------------------------------------------------------------
RUN mkdir -p /home/user/build_logs

# branch_main.log
RUN cat >/home/user/build_logs/branch_main.log <<'EOF'
BuildStart: 2023-08-15 14:23:11
[INFO] Checking dependencies
[ERROR:] Missing library xyz
[INFO] Build aborted
EOF

# branch_release.log
RUN cat >/home/user/build_logs/branch_release.log <<'EOF'
BuildStart: 2023-08-16 09:04:51
[INFO] Preparing build
[INFO] Compiling...
[FAILURE:] Unit tests failed
[ERROR:] Code signing failed
[INFO] Build failed
EOF

# branch_featureA.log
RUN cat >/home/user/build_logs/branch_featureA.log <<'EOF'
BuildStart: 2023-08-17 11:39:05
[INFO] Setup...
[INFO] Build succeeded
[INFO] Cleaning up
EOF

# Ensure the summary file is NOT present initially
RUN rm -f /home/user/build_logs/error_summary.csv || true

# ---------------------------------------------------------------------
# Make sure the non-root runtime user can read/write the workspace
# ---------------------------------------------------------------------
RUN chmod -R a+rwX /home/user

# ---------------------------------------------------------------------
# Environment variables (from %environment)
# ---------------------------------------------------------------------
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# ---------------------------------------------------------------------
# Labels (from %labels)
# ---------------------------------------------------------------------
LABEL Author="agent-setup" \
      Description="Apptainer image with predefined build logs and pytest installed for CI/CD summarisation task."

# ---------------------------------------------------------------------
# Default command (from %runscript)
# ---------------------------------------------------------------------
CMD echo "Container for mobile-app CI/CD log summarisation task." && \
    echo "Use this container to run the student solution script."