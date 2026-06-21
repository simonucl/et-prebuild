# Author="ChatGPT"
# Description="Starter container for the IT-support technician exercise with pytest pre-installed."
# This image provides:
#   - /home/user/helpdesk/tickets_raw.csv (raw ticket data)
# No other deliverable files are present; the student must create them.
# Pytest is installed so the automated grader can run its test suite.

FROM ubuntu:22.04

ENV PATH="$PATH:/usr/local/bin"

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/helpdesk

RUN cat >/home/user/helpdesk/tickets_raw.csv <<'CSVEOF'
TicketID,Submitted,Resolved,Agent,Priority,Status
1001,2023-06-01 09:15,2023-06-01 10:20,alice,HIGH,RESOLVED
1002,2023-06-01 11:05,,bob,LOW,OPEN
1003,2023-06-01 12:30,2023-06-02 08:45,charlie,MEDIUM,RESOLVED
1004,2023-06-02 09:45,,alice,HIGH,OPEN
1005,2023-06-02 10:00,2023-06-02 16:10,bob,LOW,RESOLVED
1006,2023-06-03 14:20,,charlie,MEDIUM,PENDING
1007,2023-06-03 15:55,,alice,CRITICAL,OPEN
1008,2023-06-03 16:05,2023-06-04 09:00,bob,LOW,RESOLVED
CSVEOF

RUN chmod 0755 /home/user && \
    chmod 0755 /home/user/helpdesk && \
    chmod 0644 /home/user/helpdesk/tickets_raw.csv && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN chmod 755 /home/user