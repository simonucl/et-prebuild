# Converted from Apptainer .def
FROM ubuntu:22.04

# 1. Base packages & Python tooling
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# 2. Prepare /home/user workspace and seed data
RUN mkdir -p /home/user && \
    chmod 0777 /home/user && \
    mkdir -p /home/user/data && \
    chmod 0755 /home/user/data

RUN cat > /home/user/data/service_incidents.log <<'EOF'
id,timestamp,service,host,severity,message
1001,2023-08-14T10:15:32Z,auth-api,auth01,CRITICAL,Authentication failure rate above threshold
1002,2023-08-14T10:17:05Z,billing-api,billing02,WARNING,Slow response time detected
1003,2023-08-14T10:18:44Z,auth-api,auth02,CRITICAL,Multiple 5xx errors observed
1004,2023-08-14T10:22:11Z,search-api,search01,INFO,Zero-downtime deployment completed
1005,2023-08-14T10:25:53Z,billing-api,billing01,CRITICAL,Database connection pool exhausted
1006,2023-08-14T10:27:19Z,auth-api,auth03,WARNING,Increased latency
1007,2023-08-14T10:30:07Z,search-api,search02,CRITICAL,Out of memory killed process
1008,2023-08-14T10:35:41Z,user-service,user01,INFO,Refresh tokens rotated
1009,2023-08-14T10:38:00Z,billing-api,billing03,CRITICAL,Payment gateway timeout
1010,2023-08-14T10:40:24Z,user-service,user02,WARNING,Cache miss rate increased
EOF

RUN chmod 0644 /home/user/data/service_incidents.log && \
    rm -rf /home/user/output

# Environment setup
ENV PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN chmod 755 /home/user

# Labels
LABEL Author="example@example.com"
LABEL Description="Container for CLI incident-log triage task (pytest pre-seeded)"