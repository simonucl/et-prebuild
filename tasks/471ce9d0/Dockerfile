FROM ubuntu:22.04

# Update package lists and install Python + pytest
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create /home/user and logs directory with required permissions
RUN mkdir -p /home/user/logs && \
    chmod 0777 /home/user/logs && \
    chmod 755 /home/user

# Populate the auth.log file
RUN cat > /home/user/logs/auth.log <<'EOF'
Jan 10 2025 08:23:45 server sshd[12345]: Failed password for invalid user admin from 192.168.1.10 port 54321 ssh2
Jan 10 2025 09:15:02 server sshd[23456]: Failed password for root from 203.0.113.5 port 54433 ssh2
Jan 11 2025 10:00:00 server sshd[34567]: Failed password for user john from 198.51.100.7 port 60000 ssh2
Jan 11 2025 10:05:25 server sshd[34568]: Failed password for user mike from 198.51.100.8 port 60001 ssh2
Jan 11 2025 23:59:59 server sshd[40000]: Failed password for invalid user test from 198.51.100.9 port 60002 ssh2
EOF

RUN chmod 0644 /home/user/logs/auth.log

# Help text from %help
# This Apptainer image sets up:
#   • /home/user/logs/auth.log with sample data
#   • /home/user/logs directory writable by the runtime user
#   • pytest available for the automated test harness

LABEL Author="Failed-SSH-Summary-Setup"
LABEL Description="Environment for daily failed SSH login summary task"