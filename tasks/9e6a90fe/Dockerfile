# Author: AI
# Description: Base image for SSH-key onboarding task. Installs Python, pytest and ssh-keygen; prepares writable /home/user.
# Help:
#   This container supplies:
#   - ssh-keygen (from openssh-client) so students can create keys
#   - pytest for the automated grading suite
#   The workspace /home/user is writable and initially empty of any artefacts required by the assignment.

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        openssh-client \
        ca-certificates \
    && pip3 install --no-cache-dir pytest \
    && mkdir -p /home/user \
    && chmod 0777 /home/user \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Ensure permissions as intended by runscript
RUN chmod 755 /home/user

CMD ["/bin/bash"]