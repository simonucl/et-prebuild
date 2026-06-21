FROM ubuntu:22.04

# Help:
# This Apptainer image provides the initial file-system layout required for
# ticket “INC10234”. Users will modify:
#   /home/user/it_support/firewall/allow_rules.list
# and create:
#   /home/user/it_support/logs/INC10234_action.log
# Pytest is pre-installed so automated grading can run inside the container.

LABEL Author="Auto-generated for INC10234 task setup"
LABEL Description="Apptainer image with initial state for firewall rule editing task"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/it_support/firewall && \
    mkdir -p /home/user/it_support/logs

RUN cat <<'EOF' > /home/user/it_support/firewall/allow_rules.list
# Firewall Allow Rules
ALLOW_TCP 22
ALLOW_TCP 443
EOF

RUN chmod 0777 /home/user && \
    chmod -R 0777 /home/user/it_support && \
    chmod 0666 /home/user/it_support/firewall/allow_rules.list

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH