FROM ubuntu:22.04

# Post section
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat >/home/user/user_db.csv <<'EOF'
username,uid,gid,status,fullname,home
john,1001,100,active,John Doe,/home/john
mary,1002,100,inactive,Mary Smith,/home/mary
alice,1003,100,active,Alice Jones,/home/alice
bob,1004,100,active,Bob Brown,/home/bob
eve,1005,100,inactive,Eve Adams,/home/eve
EOF

RUN chmod 0644 /home/user/user_db.csv

RUN apt-get update -qq && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Environment section
RUN chmod 755 /home/user
ENV PATH="/usr/local/bin:$PATH"

# Labels
LABEL Author="Site-Prep-Bot"
LABEL Description="Initial container for the flat-file user database task"