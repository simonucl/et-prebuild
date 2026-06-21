# Converted from Apptainer definition file
FROM ubuntu:22.04

# Install Python, pip, pytest, and prepare filesystem
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN set -e && \
    mkdir -p /home/user/reports/summary && \
    printf "Q1 financial summary\n" > /home/user/reports/report1.txt && \
    printf "Q2 financial summary\n" > /home/user/reports/report2.txt && \
    printf "Q3 details\n" > /home/user/reports/summary/quarter3.txt && \
    chmod 0777 /home/user && \
    chmod 0755 /home/user/reports /home/user/reports/summary && \
    chmod 0644 /home/user/reports/report1.txt /home/user/reports/report2.txt /home/user/reports/summary/quarter3.txt

# Labels
LABEL Author="BackupTaskSetup"
LABEL Description="Container with initial state for the backup administrator exercise"

# Run command
CMD echo "Container for the backup administrator exercise. Start a shell to begin."