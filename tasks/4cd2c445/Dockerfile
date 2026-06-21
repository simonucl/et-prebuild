FROM ubuntu:22.04

# Update package lists and install Python plus pip
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the directory structure and snapshot file
RUN mkdir -p /home/user/data

RUN cat > /home/user/data/process_snapshot.txt << 'EOF'
PID USER     COMMAND
  1 root     systemd
  2 root     kthreadd
100 daemon   some_daemon
101 daemon   another_daemon
200 user     bash
201 user     vim
202 user     python
300 user     java
400 root     sshd
401 root     sshd
402 root     cron
EOF

RUN chmod 644 /home/user/data/process_snapshot.txt && \
    chmod 755 /home/user

ENV PATH="/usr/local/bin:${PATH}"

LABEL Author="Example Author"
LABEL Purpose="Static process snapshot analysis exercise"