FROM ubuntu:22.04

# Help:
# This container provides the starting filesystem layout for the
# data-cleaning Makefile exercise. Only the raw_data directory and its
# CSV files exist; the student must create the Makefile and subsequent
# outputs. Pytest is installed so the automated checker can run.

LABEL Author="task-setup"
LABEL Description="Data-cleaning Makefile challenge – initial state only."

ENV HOME=/home/user

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        make && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN PROJECT_DIR="/home/user/data_science_project" && \
    RAW_DIR="${PROJECT_DIR}/raw_data" && \
    mkdir -p "${RAW_DIR}"

RUN PROJECT_DIR="/home/user/data_science_project" && \
    RAW_DIR="${PROJECT_DIR}/raw_data" && \
    cat > "${RAW_DIR}/sales_q1.csv" <<'EOF'
id,product,units
1,Widget,10
2,Gadget,
3,Thingamajig,5
EOF

RUN PROJECT_DIR="/home/user/data_science_project" && \
    RAW_DIR="${PROJECT_DIR}/raw_data" && \
    cat > "${RAW_DIR}/sales_q2.csv" <<'EOF'
id,product,units
4,Widget,7
5,Gadget,3
6,Thingamajig,
EOF

RUN chmod -R a+rwx /home/user/data_science_project

RUN chmod 755 /home/user