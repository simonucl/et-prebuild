FROM ubuntu:22.04

# System packages and Python tooling
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Directory structure for the exercise
RUN mkdir -p /home/user/data && \
    mkdir -p /home/user/output

# Create the required CSV source files with exact content (LF endings)
RUN cat > /home/user/data/sales_q1.csv <<'EOF'
Region,Product,Sales
East,Gadget,1200
West,Widget,800
East,Widget,950
North,Gadget,620
East,Doohickey,300
EOF

RUN cat > /home/user/data/sales_q2.csv <<'EOF'
Region,Product,Sales
South,Gadget,730
East,Gadget,660
West,Doohickey,410
East,Widget,540
East,Doohickey,200
EOF

# Permissions: make sure the non-root user inside the container can write
RUN chmod 0777 /home/user /home/user/data /home/user/output && \
    chmod 0666 /home/user/data/sales_q1.csv /home/user/data/sales_q2.csv

# Environment variables
ENV PYTHONUNBUFFERED=1

WORKDIR /home/user

CMD ["echo", "Container for the 'East-region product sales summary' exercise."]