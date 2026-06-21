FROM ubuntu:22.04

# Author ssh-task-integration

# Update package index and install required software
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        openssh-client && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    chmod 755 /home/user && \
    chown -R user:user /home/user

# IMPORTANT: Do *not* create ~/.ssh, key files, or log files here.
# The student/agent must generate them during the exercise.

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# This container image supplies a minimal Ubuntu 22.04 environment with:
#   • A non-root user "user" (home: /home/user)
#   • openssh-client for ssh-keygen
#   • pytest for automated grading
# No task artefacts are pre-created, so the exercise starts from a clean slate.

ENTRYPOINT []
CMD ["/bin/bash"]