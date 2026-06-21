FROM ubuntu:22.04

# Author "Apptainer Task Setup – SSH Compliance Audit"

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

RUN ln -sf /usr/bin/python3 /usr/bin/python

RUN mkdir -p /home/user/compliance/logs

RUN cat > /home/user/compliance/logs/audit.log <<'EOF'
2023-10-01T09:15:21Z IP=192.168.1.45 USER=root RESULT=FAIL
2023-10-01T09:15:23Z IP=192.168.1.45 USER=root RESULT=FAIL
2023-10-01T10:05:11Z IP=10.0.0.12 USER=admin RESULT=FAIL
2023-10-02T08:22:04Z IP=172.16.0.4 USER=admin RESULT=SUCCESS
2023-10-03T11:01:45Z IP=192.168.1.45 USER=root RESULT=FAIL
2023-10-04T03:14:07Z IP=203.0.113.8 USER=test RESULT=FAIL
2023-10-04T04:20:23Z IP=203.0.113.8 USER=test RESULT=FAIL
2023-10-04T05:33:18Z IP=203.0.113.8 USER=test RESULT=FAIL
2023-10-05T13:08:55Z IP=10.0.0.12 USER=admin RESULT=FAIL
2023-10-05T14:20:55Z IP=203.0.113.8 USER=test RESULT=SUCCESS
2023-10-06T07:44:33Z IP=198.51.100.2 USER=guest RESULT=FAIL
EOF

RUN chmod -R a+rwX /home/user/compliance

RUN chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH