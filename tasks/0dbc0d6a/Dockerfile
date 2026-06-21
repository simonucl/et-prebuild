FROM ubuntu:22.04

# Author penetration-test-setup
# Description: Base image for mini vulnerability-pipeline assignment
# Help:
# This container provides the initial state for the penetration-testing
# automation task. It includes:
#   • pytest (for the grading harness)
#   • /home/user/pen_test/targets.txt with the required IP addresses
# No other artefacts are pre-created.

RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir pytest

RUN mkdir -p /home/user/pen_test

RUN cat <<'EOF' >/home/user/pen_test/targets.txt
192.168.0.10
192.168.0.11
192.168.0.12
EOF

RUN chmod 755 /home/user && chmod 755 /home/user/pen_test && chmod 644 /home/user/pen_test/targets.txt

LABEL Author="penetration-test-setup"
LABEL Description="Base image for mini vulnerability-pipeline assignment"