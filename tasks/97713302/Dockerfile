FROM ubuntu:22.04

# Set environment variable
ENV DEBIAN_FRONTEND=noninteractive

# Update apt indices and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        jq \
        csvtool \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Create user and home directory
RUN useradd -m -s /bin/bash user && \
    chmod 755 /home/user

# Create the incidents directory and CSV file
RUN mkdir -p /home/user/incidents && \
    chmod 755 /home/user/incidents

RUN cat << 'CSVEOF' > /home/user/incidents/auth_failures.csv
timestamp,username,source_ip,status
2024-05-14T08:41:23Z,alice,192.168.1.10,FAILED
2024-05-14T09:02:11Z,bob,10.0.0.3,SUCCESS
2024-05-14T10:15:04Z,charlie,172.16.5.5,FAILED
2024-05-14T10:45:30Z,alice,192.168.1.10,FAILED
2024-05-14T11:00:00Z,dave,203.0.113.99,SUCCESS
CSVEOF

RUN chmod 644 /home/user/incidents/auth_failures.csv && \
    chown -R user:user /home/user/incidents

# Set working directory
WORKDIR /home/user

# Switch to user
USER user

# Labels
LABEL Author="Incidents Task Maintainer"
LABEL Description="Environment for authentication incident response task"

# Help information (as comment):
# This container provides the starting state for the "failed login" incident
# response exercise. It ensures the required CSV file is present under
# /home/user/incidents with the correct permissions and contents.
# Python3, pytest, jq, and csvtool are pre-installed for convenience.