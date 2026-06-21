FROM ubuntu:22.04

# Prepare system and install packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pip \
        sqlite3 \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/sales_analysis

# Create starter CSV file
RUN cat <<'EOF' > /home/user/projects/sales_analysis/sales_q1.csv
region,product,quantity,unit_price
North,Widget,10,2.5
South,Gadget,5,5.25
East,Widget,7,2.5
West,Gizmo,3,10.00
EOF

# Permissions
RUN chmod -R a+rwX /home/user && \
    chmod 755 /home/user

ENV PYTHONUNBUFFERED=1

# Help / labels
# Author: Task Setup Generator
# Purpose: Initial container for the sales analysis SQLite exercise
LABEL Author="Task Setup Generator" \
      Purpose="Initial container for the sales analysis SQLite exercise"