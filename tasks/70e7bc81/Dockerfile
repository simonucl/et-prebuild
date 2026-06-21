# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Container Build Script for Storage LP Task" \
      Version="1.0" \
      Description="Provides initial state (LP file, glpsol, pytest) for the student storage LP assignment."

# Post section: system setup and file creation
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        glpk-utils \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading suite
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# Create the working directory
RUN mkdir -p /home/user

# Populate the LP file using a heredoc
RUN cat > /home/user/storage_problem.lp <<'EOF'
Minimize
 obj: x1 + 2 x2 + 3 x3
Subject To
 c1: x1 + x2 + x3 >= 10
Bounds
 0 <= x1 <= 4
 0 <= x2 <= 5
 0 <= x3 <= 7
Generals
 x1 x2 x3
End
EOF

# Ensure readable permissions on the LP file and directory
RUN chmod 644 /home/user/storage_problem.lp && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

# Help:
# This container provides an initial state for the storage LP assignment,
# including glpsol (from glpk-utils), pytest, and a predefined LP file
# located at /home/user/storage_problem.lp.