# This container provides the initial state for the solver curation task.
# The repository with solver artefacts is located at /home/user/repos/solvers.

FROM ubuntu:22.04

LABEL Author="auto-generated"
LABEL Description="Environment for solver curation task with pytest pre-installed"

ENV LC_ALL=C.UTF-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN set -e && \
    mkdir -p /home/user/repos/solvers && \
    chmod 755 /home/user && \
    chmod 755 /home/user/repos && \
    chmod 755 /home/user/repos/solvers

RUN set -e && \
    cd /home/user/repos/solvers && \
    truncate -s 1536000   glpk-5.0-linux-x86_64.tar.gz && \
    truncate -s 1658880   glpk-5.1-linux-x86_64.tar.gz && \
    truncate -s 307200000 cplex-12.10-linux-x86_64.bin && \
    truncate -s 319979520 cplex-22.1-linux-x86_64.bin && \
    truncate -s 286720000 gurobi-9.1.1-linux-x86_64.tar.gz && \
    truncate -s 325058560 gurobi-10.0.0-linux-x86_64.tar.gz && \
    chmod 644 /home/user/repos/solvers/*