FROM ubuntu:22.04

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/helpdesk && \
    chmod 0755 /home/user && \
    chmod 0777 /home/user/helpdesk

RUN cat > /home/user/helpdesk/tickets.csv << 'EOF'
TicketID,User,Status,Priority,Date
101,alice,Open,High,18/09/2023
102,bob,Closed,Low,18-09-2023
103,charlie,Open,Medium,2023/09/17
104,dave,Closed,High,2023-09-17
101,alice,Open,High,18/09/2023
105,alice,Closed,Low,2023-09-16
106,erin,Open,High,16-09-2023
107,frank,Open,Low,2023/09/15
106,erin,Open,High,16-09-2023
EOF

RUN chmod 0644 /home/user/helpdesk/tickets.csv && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH