FROM ubuntu:22.04

# Install required packages and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        findutils \
        coreutils \
        tzdata && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create non-root user "user"
RUN useradd -m -u 1000 -s /bin/bash user

# Build initial log directory tree and files
# Directories
RUN install -o user -g user -d /home/user/microservices/logs/serviceA && \
    install -o user -g user -d /home/user/microservices/logs/serviceB

# Old log files (mtime > 7 days)
RUN touch -a -m -t 202301100000 /home/user/microservices/logs/serviceA/access-2023-01-10.log && \
    touch -a -m -t 202301090000 /home/user/microservices/logs/serviceA/error-2023-01-09.log && \
    touch -a -m -t 202301080000 /home/user/microservices/logs/serviceB/app-2023-01-08.log

# Recent log files (mtime ≤ 7 days)
RUN touch /home/user/microservices/logs/serviceA/current.log && \
    touch /home/user/microservices/logs/serviceB/debug-2023-12-31.log

# Ensure ownership and correct permissions
RUN chown -R user:user /home/user && \
    chmod -R u+rwX,go+rX /home/user && \
    chmod 755 /home/user

# Environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8