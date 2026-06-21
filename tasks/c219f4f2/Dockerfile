FROM ubuntu:22.04

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Ensure a user/group with UID/GID 1000 exists (most host users use 1000)
RUN if ! getent group 1000 >/dev/null 2>&1; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 user; \
    fi

# Create /home/user hierarchy if it doesn't already exist
RUN mkdir -p /home/user

# Secrets directory and token file
RUN install -d -m 0700 /home/user/secrets && \
    printf 'SECRET_TOKEN_DO_NOT_SHARE\n' > /home/user/secrets/api_token.txt && \
    chmod 0644 /home/user/secrets/api_token.txt

# Rotation directory (log file intentionally NOT created)
RUN install -d -m 0700 /home/user/rotation

# Ensure the runtime user owns everything under /home/user
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

ENV PYTHONUNBUFFERED=1
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin:/bin:/sbin

LABEL Author="Apptainer Task Preparation"
LABEL Description="Container prepared for API token rotation exercise with pytest installed."