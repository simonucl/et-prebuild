FROM ubuntu:22.04

# Labels
LABEL Author="ans"

# Update package index and install Python + pip
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create required directory
RUN mkdir -p /home/user/logs

# Create log file with expected content
RUN cat > /home/user/logs/auth.log <<'EOF'
Jan 21 10:10:10 host sshd[12345]: Failed password for invalid user admin from 192.168.1.20 port 55874 ssh2
Jan 21 10:10:12 host sshd[12346]: Failed password for root from 192.168.1.30 port 55875 ssh2
Jan 21 10:10:13 host sshd[12347]: Accepted password for user1 from 192.168.1.40 port 55876 ssh2
Jan 21 10:10:15 host sshd[12348]: Failed password for user2 from 192.168.1.50 port 55877 ssh2
Jan 21 11:00:00 host sshd[12349]: Failed password for invalid user test from 192.168.1.60 port 55878 ssh2
Jan 21 11:05:00 host sshd[12350]: Failed password for user3 from 192.168.1.70 port 55879 ssh2
Jan 21 12:00:00 host sshd[12351]: Accepted password for user4 from 192.168.1.80 port 55880 ssh2
EOF

# Ensure directory is writable by any user running inside the container
RUN chmod 0777 /home/user/logs && \
    chmod 0644 /home/user/logs/auth.log && \
    chmod 755 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Set working directory
WORKDIR /home/user

# Default command
CMD ["echo", "Container for SOC log-analysis exercise.  Run your commands inside the shell."]