FROM ubuntu:22.04

# Basic tooling
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create non-root user "user" (UID/GID 1000)
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Initial file system state required by the tests
# Tickets directory and queue file
RUN mkdir -p /home/user/tickets

RUN cat > /home/user/tickets/ticket_queue.csv <<'EOF'
TicketID,Package,RequiredVersion,Action
101,alpha,1.2.0,upgrade
102,beta,N/A,remove
103,delta,4.5.6,install
104,gamma,0.9.0,downgrade
EOF

# Package repository with the three initial package version directories
RUN mkdir -p /home/user/pkgdb && \
    for pkg in alpha-1.0.0 beta-2.3.4 gamma-0.9.8; do \
        mkdir -p "/home/user/pkgdb/${pkg}"; \
    done

# Ownership & permissions: make sure the non-root user can modify inside /home/user
RUN chown -R user:user /home/user && \
    chmod -R u+rwX,go+rX /home/user

# Environment variables
ENV PATH=/home/user/.local/bin:$PATH

# Set permissions on /home/user at runtime and default command
RUN chmod 755 /home/user

CMD ["/bin/bash"]