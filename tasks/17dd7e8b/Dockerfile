FROM ubuntu:22.04

# Help:
# This container sets up the initial environment for the “user-level systemd service” task.
# It pre-installs pytest for the grader, prepares the heartbeat utility script,
# and creates the expected directory layout under /home/user without the output artefacts.

LABEL Author="production"

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip \
    && pip3 install --no-cache-dir pytest \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/utils \
    && mkdir -p /home/user/.config/systemd/user

RUN cat > /home/user/utils/heartbeat.sh <<'EOF'
#!/usr/bin/env bash
date +"%Y-%m-%d %H:%M:%S - heartbeat"
EOF

RUN chmod 755 /home/user/utils/heartbeat.sh

RUN chmod 755 /home/user/utils \
    && chmod 700 /home/user/.config/systemd/user \
    && rm -f /home/user/.config/systemd/user/my_utility.service \
              /home/user/my_utility_service_creation.log