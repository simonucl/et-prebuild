FROM ubuntu:22.04

# Help:
# This Apptainer image provides the initial environment for the help-desk
# CSV processing assignment. It contains:
#   • /home/user/data/support_tickets.csv  (read-only input file)
#   • /home/user/output/                   (writeable output directory)
# Python and pytest are installed for automated grading.

# Labels
LABEL Author="example"
LABEL Description="Container for awk/sed text-processing task (support tickets)"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data && \
    mkdir -p /home/user/output

RUN cat > /home/user/data/support_tickets.csv <<'EOF'
ticket_id,created_date,assignee,status
TCK-1001,01/13/2022,alice,OPEN
TCK-1002,01/20/2022,bob,CLOSED
TCK-1003,02/05/2022,charlie,OPEN
TCK-1004,03/14/2022,dan,CLOSED
TCK-1005,03/18/2022,alice,CLOSED
TCK-1006,04/07/2023,bob,OPEN
TCK-1007,05/11/2023,charlie,CLOSED
TCK-1008,06/22/2023,dan,OPEN
TCK-1009,07/19/2023,alice,CLOSED
TCK-1010,08/01/2023,bob,OPEN
EOF

RUN chmod 644 /home/user/data/support_tickets.csv
RUN chmod 777 /home/user/output
RUN chmod -R a+rX /home/user