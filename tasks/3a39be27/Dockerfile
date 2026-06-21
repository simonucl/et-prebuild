FROM ubuntu:22.04

# Help section
# Default runscript just opens a shell

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    if ! getent group user >/dev/null 2>&1; then groupadd -g 1000 user; fi && \
    if ! id -u user >/dev/null 2>&1; then useradd -m -u 1000 -g user -s /bin/bash user; fi && \
    chown -R user:user /home/user && \
    rm -rf /var/lib/apt/lists/*

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

RUN chmod 755 /home/user

CMD ["/bin/bash"]