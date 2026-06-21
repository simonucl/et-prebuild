FROM ubuntu:22.04

# Help:
# This container provides:
#   • Python 3 interpreter
#   • pip & venv module
#   • pytest (system-wide)
#   A non-root user “user” with home directory /home/user is present.
#   No project artefacts for the assignment are pre-created; the student
#   must generate them during their solution steps.

LABEL Author="user"
LABEL Description="Container for the api-test programming task – initial clean state with pytest installed."

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

RUN useradd --create-home --shell /bin/bash user && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

CMD ["bash"]