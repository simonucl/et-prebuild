# Help: Converted from Apptainer definition using localimage ubuntu_22.04.sif
FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project/test_data

RUN cat <<'EOF' > /home/user/project/test_data/raw_metrics.csv
test_case,module,status,execution_time
TC001,login,pass,2.1
TC002,signup,fail,3.4
TC003,logout,pass,1.7
EOF

RUN chmod 777 /home/user/project/test_data && \
    chmod 666 /home/user/project/test_data/raw_metrics.csv && \
    chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH