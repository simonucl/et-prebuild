FROM ubuntu:22.04

# Help text from Apptainer %help
# This container provides the initial environment for resolving Ticket #425.
# A YAML configuration file and helper script are located under:
#   /home/user/services/app-service/
# Pytest is pre-installed so the automated grader can verify the initial state.

RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/services/app-service

RUN cat <<'EOF' > /home/user/services/app-service/config.yml
# Application service configuration
maintenance: true
version: 1.4.2
EOF

RUN cat <<'EOF' > /home/user/services/app-service/restart.sh
#!/bin/bash
# Simulated restart helper
echo "app-service restarted" > /home/user/services/app-service/restart.log
EOF

RUN chmod 0755 /home/user/services/app-service/restart.sh && \
    chmod 0666 /home/user/services/app-service/config.yml && \
    chmod -R 0777 /home/user && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH