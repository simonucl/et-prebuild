FROM ubuntu:22.04

# Author: edge_task_builder
# Description: Container supplying initial state for edge_project deployment exercise.

ENV PATH=/usr/local/bin:$PATH
ENV PYTHONIOENCODING=utf-8

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        ca-certificates \
        tzdata

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/edge_project

RUN cat > /home/user/edge_project/devices_master.tsv <<'EOF'
device_id	model	firmware_version	ip_address	uptime_hours	city	ready_for_deploy
gw-001	A1	1.0.3	192.168.0.11	240	NewYork	yes
gw-002	B2	1.0.1	10.0.0.50	12	Berlin	no
gw-003	A1	1.0.4	192.168.0.30	48	NewYork	yes
gw-004	C3	1.2.0	172.16.1.10	5	Tokyo	yes
gw-005	B2	1.0.1	10.0.0.60	96	Berlin	yes
EOF

RUN chmod 755 /home/user /home/user/edge_project && \
    chmod 644 /home/user/edge_project/devices_master.tsv

CMD echo "Container for edge_project task. Enter the shell to begin work." && /bin/bash -l