FROM ubuntu:22.04

# Help text
# This container sets up the initial filesystem and installs pytest so that
# students can focus solely on writing their remediation script.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/ops

RUN cat > /home/user/ops/docker_ps_2023-10-07T1200.txt <<'EOF'
CONTAINER ID   IMAGE           COMMAND                  CREATED        STATUS                       PORTS                    NAMES
d1e3f9c1b2fe   myorg/api:1.4   "gunicorn app:app"       3 hours ago    Exited (1) 25 minutes ago                            api_1
b4c2a9d6e7ff   myorg/web:2.0   "nginx -g 'daemon of…"   3 hours ago    Up 3 hours                  0.0.0.0:80->80/tcp       web_1
f9a4c7d8e9ab   myorg/worker    "python worker.py"       3 hours ago    Exited (137) 15 minutes ago                          worker_1
EOF

RUN chmod 644 /home/user/ops/docker_ps_2023-10-07T1200.txt

RUN chmod 755 /home/user

LABEL Author="ChatGPT"
LABEL Description="Initial state for Docker remediation task"