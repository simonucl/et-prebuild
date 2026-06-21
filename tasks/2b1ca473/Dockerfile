# Converted from Apptainer definition
FROM ubuntu:22.04

# Basic utilities and Python
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN pip3 install --no-cache-dir pytest

# Create directory hierarchy and set permissions
RUN mkdir -p /home/user/compliance/raw_logs && \
    chmod 0755 /home/user && \
    chmod -R 0755 /home/user/compliance

# Populate login_events.csv
RUN cat > /home/user/compliance/raw_logs/login_events.csv <<'CSV'
event_id,timestamp,user,action,source_ip
LE1,2023-04-01T09:15:27Z,alice,login,192.168.1.10
LE2,2023-04-01T12:47:03Z,bob,login,192.168.1.11
LE3,2023-04-01T17:05:44Z,alice,logout,192.168.1.10
LE4,2023-04-02T08:01:09Z,charlie,login,192.168.1.12
LE5,2023-04-02T11:30:17Z,bob,logout,192.168.1.11
CSV

# Populate file_access.csv
RUN cat > /home/user/compliance/raw_logs/file_access.csv <<'CSV'
event_id,timestamp,user,file_path,operation
FA1,2023-04-01T10:03:12Z,alice,/srv/docs/confidential.pdf,read
FA2,2023-04-01T10:15:55Z,alice,/srv/docs/confidential.pdf,write
FA3,2023-04-01T13:22:40Z,bob,/srv/spreadsheets/budget.xlsx,read
FA4,2023-04-02T09:12:06Z,charlie,/srv/scripts/deploy.sh,read
FA5,2023-04-02T09:45:55Z,charlie,/srv/scripts/deploy.sh,write
FA6,2023-04-02T12:11:33Z,bob,/srv/spreadsheets/budget.xlsx,write
CSV

# Set file permissions
RUN chmod 0644 /home/user/compliance/raw_logs/login_events.csv && \
    chmod 0644 /home/user/compliance/raw_logs/file_access.csv && \
    chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# No default run action (equivalent to %runscript)
CMD echo "Container for the Compliance Audit task – no default action defined."