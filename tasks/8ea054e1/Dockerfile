# Converted from Apptainer definition file
FROM ubuntu:22.04

# Update apt database and install Python & pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the runtime tests
RUN pip3 install --no-cache-dir pytest

# Create directory structure for the DNS-log assignment
RUN mkdir -p /home/user/logs

# Create the sample DNS traffic log
RUN cat >/home/user/logs/dns_traffic.log <<'EOF'
2023-03-01T12:00:01Z example.com 93.184.216.34
2023-03-01T12:00:02Z example.com 93.184.216.34
2023-03-01T12:00:03Z localhost 127.0.0.1
2023-03-01T12:00:04Z example.net 93.184.216.34
2023-03-01T12:00:05Z example.com 93.184.216.35
2023-03-01T12:00:06Z example.net 93.184.216.34
EOF

# Ensure readability for non-root users
RUN chmod -R 0755 /home/user

ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Help text from %runscript
# Container for the DNS log-analysis task.
# Open a shell with:
#    apptainer exec <image>.sif /bin/bash