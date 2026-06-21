FROM ubuntu:22.04

# Help:
# chmod 755 /home/user
# Container for the “SSH-key installation & Kubernetes-Secret” task.
# Pre-seeded keys are available under /home/user/preseed/.
# Pytest is installed for the grader’s test-suite.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user && \
    chmod 0777 /home/user

RUN mkdir -p /home/user/preseed && \
    chmod 0755 /home/user/preseed

RUN printf 'myprivatekey\n' > /home/user/preseed/id_ed25519 && \
    chmod 0644 /home/user/preseed/id_ed25519

RUN printf 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIG15cHVibGlja2V5 user@training\n' \
    > /home/user/preseed/id_ed25519.pub && \
    chmod 0644 /home/user/preseed/id_ed25519.pub

RUN apt-get clean && rm -rf /var/lib/apt/lists/*