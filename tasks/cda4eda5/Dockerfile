FROM ubuntu:22.04

# Labels
LABEL Author="dev-utils-exercise"
LABEL Description="Initial state for the \"dev-utils\" scripting exercise"

# Help information (as comments):
# This container provides the starting environment for the "dev-utils" exercise.
# It contains:
#   • /home/user/dev-utils/raw_ips.log
#   • /home/user/dev-utils/users.csv
# No other artefacts are present.
# Pytest is pre-installed so the automatic grader can run its test suite.

RUN set -eux && \
    # Install Python tooling for the test suite
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip python3-setuptools && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial exercise directory structure
RUN mkdir -p /home/user/dev-utils

# Create raw_ips.log
RUN cat <<'EOF' > /home/user/dev-utils/raw_ips.log
2024-02-09 12:01:11 Connection from 192.168.1.10: accepted
2024-02-09 12:01:12 8.8.8.8 requested /favicon.ico
WARN: suspicious activity from 10.0.0.5
Client at 172.16.0.3 disconnected
192.168.1.12 - - [09/Feb/2024:12:01:13] "GET /index.html"
203.0.113.25 - possible abuse report
INFO [client 10.1.2.3] request processed
192.168.1.10 - - [09/Feb/2024:12:01:15] "GET /dashboard"
ERROR - invalid credentials from 10.0.0.5
Ping from 192.168.1.100 successful
Session start for 100.64.0.1
198.51.100.42 contacted support endpoint
Heartbeat ok from 172.20.14.2
Random noise without address
Client 192.0.2.123 disconnected
Another line with IP 192.168.1.12
EOF

# Create users.csv
RUN cat <<'EOF' > /home/user/dev-utils/users.csv
id,name,department,status
1,Alice Smith,Engineering,active
2,Bob Jones,Engineering,active
3,Carol White,Engineering,inactive
4,David Black,HR,active
5,Eva Green,Marketing,active
6,Frank Brown,Sales,active
7,Grace Miller,Sales,active
8,Hank Wilson,Sales,active
9,Ian Clark,Marketing,inactive
10,Judy Adams,Engineering,active
11,Kate Lewis,Engineering,active
12,Larry Young,Engineering,active
13,Mona Hall,HR,inactive
14,Nick King,Marketing,active
EOF

# Ensure permissions allow the (non-root) learner to create new files
RUN chmod 777 /home/user && \
    chmod 777 /home/user/dev-utils && \
    chmod 644 /home/user/dev-utils/raw_ips.log /home/user/dev-utils/users.csv

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user