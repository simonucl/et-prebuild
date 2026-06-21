FROM ubuntu:22.04

# Help:
# This Apptainer image provides the initial state for the “network log filtering”
# exercise. A canonical connection log is placed at
# /home/user/network/logs/conn.log
# and an empty output directory is available at
# /home/user/network/output/
# Python 3 and pytest are pre-installed for automated grading.

LABEL Author="ExampleAutomation"
LABEL Description="Environment for regex-based log filtering task (pytest included)"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/network/logs && \
    mkdir -p /home/user/network/output

RUN cat > /home/user/network/logs/conn.log <<'EOF'
2023-09-14T23:58:12Z router=sfo-gw1 src=10.0.0.2 dst=8.8.8.8 proto=ICMP conn_status=OK latency=34ms
2023-09-15T00:01:44Z router=nyc-core src=172.16.4.89 dst=1.1.1.1 proto=TCP conn_status=FAIL err=101 detail="SYN timeout"
2023-09-15T00:02:53Z router=lon-edge src=192.168.1.4 dst=8.8.4.4 proto=UDP conn_status=OK
2023-09-15T01:15:22Z router=nyc-core src=10.10.10.10 dst=142.250.72.238 proto=TCP conn_status=FAIL err=104 detail="RST received"
2023-09-15T02:47:03Z router=sfo-gw1 src=10.0.0.3 dst=198.41.0.4 proto=UDP conn_status=FAIL err=108 detail="Port unreachable"
2023-09-15T03:10:37Z router=lon-edge src=192.168.1.22 dst=8.8.8.8 proto=ICMP conn_status=FAIL err=101 detail="TTL exceeded"
2023-09-15T04:21:12Z router=nyc-core src=172.16.5.5 dst=9.9.9.9 proto=TCP conn_status=FAIL err=104 detail="RST received"
2023-09-15T04:45:44Z router=sfo-gw1 src=10.0.0.25 dst=8.8.4.4 proto=UDP conn_status=OK
2023-09-15T05:33:19Z router=lon-edge src=192.168.1.42 dst=8.8.4.4 proto=UDP conn_status=FAIL err=108 detail="Timeout"
2023-09-15T06:55:01Z router=nyc-core src=10.10.10.11 dst=142.250.72.238 proto=TCP conn_status=FAIL err=101 detail="SYN timeout"
2023-09-15T08:00:00Z router=lon-edge src=192.168.1.45 dst=8.8.8.8 proto=ICMP conn_status=OK latency=37ms
2023-09-15T09:09:09Z router=sfo-gw1 src=10.0.0.50 dst=198.41.0.4 proto=UDP conn_status=FAIL err=104 detail="Unknown"
2023-09-15T10:10:10Z router=nyc-core src=172.16.5.6 dst=1.1.1.1 proto=TCP conn_status=FAIL err=108 detail="ECN failure"
2023-09-15T11:11:11Z router=lon-edge src=192.168.1.46 dst=9.9.9.9 proto=UDP conn_status=OK
2023-09-16T00:00:00Z router=sfo-gw1 src=10.0.0.2 dst=8.8.8.8 proto=ICMP conn_status=FAIL err=104 detail="Next-day test"
EOF

RUN chmod 0755 /home/user && \
    chmod -R 0755 /home/user/network && \
    chmod 0644 /home/user/network/logs/conn.log