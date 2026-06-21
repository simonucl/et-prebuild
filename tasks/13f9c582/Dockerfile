FROM ubuntu:22.04

# Install Python, pip, and clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create user
RUN useradd -m -u 1000 -s /bin/bash user

# Create logs directory
RUN mkdir -p /home/user/logs

# Create auth.log with heredoc
RUN cat > /home/user/logs/auth.log <<'EOF'
May 15 10:22:34 server sshd[12345]: Failed password for invalid user admin from 192.168.1.10 port 51122 ssh2
May 15 10:23:01 server sshd[12346]: Failed password for root from 203.0.113.5 port 42311 ssh2
May 15 10:24:07 server sshd[12347]: Accepted password for user1 from 192.0.2.7 port 38712 ssh2
May 15 10:25:12 server sshd[12348]: Failed password for root from 203.0.113.5 port 42319 ssh2
May 15 10:26:14 server sshd[12349]: Failed password for invalid user test from 198.51.100.55 port 53345 ssh2
May 15 10:27:18 server sshd[12350]: Failed password for invalid user admin from 192.168.1.10 port 51159 ssh2
May 15 10:28:30 server sshd[12351]: Accepted password for user2 from 203.0.113.8 port 42229 ssh2
May 15 10:29:02 server sshd[12352]: Failed password for root from 203.0.113.8 port 42235 ssh2
EOF

# Fix ownership and permissions
RUN chown -R 1000:1000 /home/user && \
    chmod 755 /home/user && \
    chmod 755 /home/user/logs && \
    chmod 644 /home/user/logs/auth.log

# Environment variables
ENV PATH="/home/user/.local/bin:$PATH"
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Labels
LABEL Author="example@example.com"
LABEL Description="Container for SSH incident-response counting exercise."

# Run script equivalent
CMD echo "This container is intended for the SSH incident-response exercise." && \
    echo "Open a shell with:  docker run -it <image> /bin/bash"