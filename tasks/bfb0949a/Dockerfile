# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help: No special help text provided in the original file

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        tar \
        gzip \
        coreutils && \
    rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/hardening

RUN chmod 755 /home/user && \
    chmod 755 /home/user/hardening

RUN printf 'PasswordAuthentication no\nPermitRootLogin no\n' > /home/user/hardening/sshd_config

RUN printf 'net.ipv4.ip_forward = 0\nkernel.randomize_va_space = 2\n' > /home/user/hardening/sysctl.conf

RUN chmod 644 /home/user/hardening/sshd_config /home/user/hardening/sysctl.conf

ENV HOME=/home/user

CMD ["/bin/bash"]