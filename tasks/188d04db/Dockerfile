FROM ubuntu:22.04

# Help:
# This Apptainer image provides the minimal environment required for the
# student to carry out the firewall artefact task.
# It intentionally contains NO pre-created firewall directories or files.

LABEL Author="Task Preparer"
LABEL Description="Base image for firewall artefact-creation task. Contains Python, pytest, and iptables; no firewall artefacts are pre-created."

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home || true

RUN set -eux && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        iptables && \
    pip3 install --no-cache-dir pytest && \
    useradd -m -s /bin/bash user && \
    chown -R user:user /home/user && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*