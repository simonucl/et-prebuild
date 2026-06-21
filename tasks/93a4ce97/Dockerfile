FROM ubuntu:22.04

# Base OS packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
        apt-get install -y --no-install-recommends \
            python3 \
            python3-pip \
            ca-certificates \
            tzdata && \
    pip3 install --no-cache-dir pytest

# Non-privileged user that the exercise will run under
# UID/GID 1000 is the conventional first regular account on Ubuntu
RUN if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -u 1000 -d /home/user -s /bin/bash -m user; \
    fi

# Exercise initial filesystem state - Directories
RUN mkdir -p /home/user/logs && \
    mkdir -p /home/user/output && \
    chmod 0755 /home/user/logs && \
    chmod 0775 /home/user/output

# Raw probe log with exact content (Unix LF line endings)
RUN cat >/home/user/logs/ping_results.log <<'EOF'
2023-04-01T12:00:01Z|router1|8.8.8.8|24|reachable
2023-04-01T12:05:01Z|router1|1.1.1.1|25|reachable
2023-04-01T12:10:01Z|router1|8.8.4.4|27|reachable
2023-04-01T12:15:01Z|router1|208.67.222.222|-|unreachable
2023-04-01T12:20:01Z|router1|8.8.8.8|26|reachable
2023-04-01T12:25:01Z|router1|1.1.1.1|-|unreachable
2023-04-01T12:30:01Z|router1|8.8.4.4|29|reachable
2023-04-01T12:35:01Z|router1|208.67.222.222|28|reachable
EOF

RUN chmod 0644 /home/user/logs/ping_results.log

# Ensure ownership so the non-root user can modify /home/user/output later
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user

CMD ["/bin/bash"]