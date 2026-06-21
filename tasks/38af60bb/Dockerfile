FROM ubuntu:22.04

# Help / labels
LABEL Author="auditors-team"
LABEL Description="Container preset for INI audit-log assignment (pre-task state only)"
LABEL Version="1.0"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        python3-setuptools && \
    pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest && \
    if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi && \
    mkdir -p /home/user/compliance && \
    chmod 0755 /home/user/compliance

RUN cat <<'EOF' > /home/user/compliance/app.conf
[Security]
encryption = AES256
password_policy = strong

[Network]
port = 443
tls  = enabled

[Database]
backup = daily
EOF

RUN chmod 0644 /home/user/compliance/app.conf

RUN rm -rf /home/user/compliance/audit || true

RUN chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Runscript equivalent
CMD echo "This container is prepared for the INI audit-log assignment." && \
    echo "Invoke your commands with:  docker run <image> <cmd>"