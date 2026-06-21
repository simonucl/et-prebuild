FROM ubuntu:22.04

# Help section from Apptainer
# Default runscript: execute whatever the caller supplied

ENV PATH="/home/user/.local/bin:${PATH}"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN if ! id -u user >/dev/null 2>&1; then useradd -m -s /bin/bash user; fi

RUN install -d -m 0755 /home/user/microservices

RUN cat > /home/user/microservices/services.txt <<'EOF'
auth
api
front
EOF

RUN chown -R user:user /home/user && chmod 755 /home/user

CMD ["bash", "-c", "exec \"$@\"", "--"]