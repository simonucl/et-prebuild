# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------
# Install Python, pip, locales, certificates, and pytest
# ------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        locales && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------
# Create home directory and ticket data directories
# ------------------------------------------------------------
RUN mkdir -p /home/user/tickets

# open_tickets.csv
RUN cat > /home/user/tickets/open_tickets.csv <<'CSV_EOF'
ticket_id,priority,assigned_to,customer,issue_type,status
TCK-1001,High,alice,Acme Corp,Network,Open
TCK-1002,Medium,bob,Globex Inc,Hardware,Open
TCK-1003,Low,,Initech,Software,Open
TCK-1004,High,charlie,"A&B Consulting",Network,Open
CSV_EOF

# closed_tickets.csv
RUN cat > /home/user/tickets/closed_tickets.csv <<'CSV_EOF'
ticket_id,resolution_time_min,assigned_to,customer,issue_type,status
TCK-0901,45,dan,Acme Corp,Network,Closed
TCK-0902,120,alice,Globex Inc,Hardware,Closed
TCK-0903,30,alice,Initech,Software,Closed
TCK-0904,15,bob,Acme Corp,Hardware,Closed
CSV_EOF

# Ensure writable permissions for ticket directory and proper home permissions
RUN chmod -R 0777 /home/user/tickets && \
    chmod 755 /home/user

# ------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# ------------------------------------------------------------
# Labels
# ------------------------------------------------------------
LABEL Author="ticket-processing-setup" \
      Description="Base image for the ticket-processing exercise with initial CSV data and pytest installed."

# ------------------------------------------------------------
# Help
# This image provides the starting environment for the
# “ticket-processing” CLI exercise.
#   • /home/user/tickets/open_tickets.csv
#   • /home/user/tickets/closed_tickets.csv
# Pytest is pre-installed for the grading harness.
# ------------------------------------------------------------