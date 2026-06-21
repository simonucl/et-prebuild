FROM ubuntu:22.04

# Author: Automation-Workflow Specialist
# Description: Base image for dotenv + Bash workflow exercise. Provides writable /home/user, Bash, and pytest.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user

ENV PATH=/home/user/.local/bin:$PATH

CMD ["bash"]