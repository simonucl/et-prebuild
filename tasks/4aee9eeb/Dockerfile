FROM ubuntu:22.04

# Help:
# This container provides the initial filesystem state for the assignment:
#   • Directories /home/user/data and /home/user/monitoring
#   • The raw CSV at /home/user/data/raw_sales.csv
# Pytest is installed so the automated grader can run its tests.

LABEL Author="Your Name"
LABEL Description="Starter container for the data-cleaning and monitoring assignment. Includes pytest and the required raw dataset."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data && \
    mkdir -p /home/user/monitoring && \
    chmod 777 /home/user && \
    chmod 777 /home/user/data && \
    chmod 777 /home/user/monitoring

RUN cat > /home/user/data/raw_sales.csv <<'EOF'
id,product,price,quantity
1,Widget,19.99,5
2,Gadget,,3
3,Thingamabob,4.99,
4,Widget,19.99,2
5,Gizmo,8.49,0
EOF

RUN chmod 644 /home/user/data/raw_sales.csv

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH