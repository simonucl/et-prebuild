FROM ubuntu:22.04

# Help / descriptive metadata
LABEL author="Compliance Audit Container"
LABEL description="Environment for SHA-256 compliance audit exercise with pytest pre-installed."

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/audit_samples

RUN printf 'test' > /home/user/audit_samples/archive1.tar.gz
RUN printf 'test' > /home/user/audit_samples/config.cfg
RUN printf 'test' > /home/user/audit_samples/script.sh

RUN cat > /home/user/audit_samples/reference.sha256 <<'EOF'
9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  archive1.tar.gz
9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  config.cfg
0000000000000000000000000000000000000000000000000000000000000000  script.sh
EOF

RUN chmod -R 755 /home/user

RUN if ! id -u user >/dev/null 2>&1; then \
        useradd -m -d /home/user -s /bin/bash user; \
    fi

RUN chown -R user:user /home/user

USER user
WORKDIR /home/user