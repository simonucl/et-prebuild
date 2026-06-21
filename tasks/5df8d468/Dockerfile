# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from %labels section
LABEL Author="ComplianceTaskSetup"
LABEL Description="Container for solver audit task with pytest pre-installed"

# Post-installation steps
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/opt_solvers && \
    echo "2.10.7" > /home/user/opt_solvers/cbc.version && \
    echo "5.0" > /home/user/opt_solvers/glpk.version && \
    echo "9.6" > /home/user/opt_solvers/ortools.version && \
    chmod 777 /home/user && \
    chmod 755 /home/user/opt_solvers && \
    chmod 644 /home/user/opt_solvers/*.version

# %help
# Container for solver audit task with pytest pre-installed