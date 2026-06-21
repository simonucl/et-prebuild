# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Author: "Ticket Frequency Report – Container Setup"
# Description: "Provides initial log files and pytest for automated grading."

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/tickets && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/tickets

RUN cat > /home/user/tickets/2023-10-01.log << 'EOF'
TCKT-1001, alice, NET-001
TCKT-1002, bob, PRN-404
TCKT-1003, carol, NET-001
TCKT-1004, dave, SEC-900
TCKT-1005, erin, NET-001
TCKT-1006, frank, PRN-404
EOF

RUN cat > /home/user/tickets/2023-10-02.log << 'EOF'
TCKT-1007, george, SEC-900
TCKT-1008, hannah, SEC-900
TCKT-1009, ian, NET-001
TCKT-1010, jane, PRN-404
TCKT-1011, kevin, NET-001
TCKT-1012, laura, PRN-404
TCKT-1013, mike, NET-001
TCKT-1014, nancy, NET-001
EOF

RUN chmod 0666 /home/user/tickets/2023-10-01.log && \
    chmod 0666 /home/user/tickets/2023-10-02.log && \
    chmod 755 /home/user

# Help:
# This container supplies the initial state for the "Ticket Frequency Report" exercise:
# • Two raw log files live in /home/user/tickets
# • The directory is writable so that learners can create issue_summary.txt
# • pytest is pre-installed for the automated grading system.