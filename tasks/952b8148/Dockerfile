FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer build script"
LABEL Description="Capacity-planner exercise environment with pytest pre-installed"

# Environment variables
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

# System setup
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare filesystem
RUN mkdir -p /home/user/projects/capplan

# resources.yaml
RUN cat > /home/user/projects/capplan/resources.yaml <<'YAML'
servers:
  - name: db01
    cpu: 4
    memory: 16
  - name: web01
    cpu: 2
    memory: 8
YAML

# thresholds.toml
RUN cat > /home/user/projects/capplan/thresholds.toml <<'TOML'
[cpu]
warning = 70
critical = 90

[memory]
warning = 75
critical = 95
TOML

# Permissions
RUN chmod -R 0777 /home/user/projects && \
    chmod 755 /home/user

WORKDIR /home/user