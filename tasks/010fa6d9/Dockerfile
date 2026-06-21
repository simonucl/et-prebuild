FROM ubuntu:22.04

# Help text
# Container for ticket #5502 exercise.
# It contains the initial cluster_status data and pytest pre-installed.

LABEL Author="IT-Support-Task-Apptainer"
LABEL Ticket="5502"

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    TICKET_DIR="/home/user/tickets/ticket-5502" && \
    STATUS_DIR="$TICKET_DIR/cluster_status" && \
    mkdir -p "${STATUS_DIR}"

RUN cat > /home/user/tickets/ticket-5502/cluster_status/node-alpha.status <<'EOF'
SERVICE=db
STATE=OK
EOF

RUN cat > /home/user/tickets/ticket-5502/cluster_status/node-beta.status <<'EOF'
SERVICE=db
STATE=FAIL
EOF

RUN cat > /home/user/tickets/ticket-5502/cluster_status/node-gamma.status <<'EOF'
SERVICE=db
STATE=OK
EOF

RUN rm -f /home/user/tickets/ticket-5502/resolution.log

RUN chmod -R a+rwX /home/user/tickets

RUN chmod 755 /home/user

CMD echo "Container for ticket #5502. Use this environment to solve the task."