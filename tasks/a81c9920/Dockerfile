FROM ubuntu:22.04

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/metrics/raw && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/metrics && \
    chmod 0777 /home/user/metrics/raw

RUN cat > /home/user/metrics/raw/dashboard_metrics.csv <<'EOF'
2023-10-31T01:00:00Z,auth-service,/login,120,1
2023-10-31T01:00:01Z,auth-service,/login,105,1
2023-10-31T01:00:02Z,auth-service,/login,200,0
2023-10-31T01:10:00Z,order-service,/checkout,350,1
2023-10-31T01:10:05Z,order-service,/checkout,400,0
2023-10-31T01:15:00Z,order-service,/checkout,360,1
2023-10-31T01:20:00Z,order-service,/checkout,370,1
2023-10-31T01:25:00Z,order-service,/checkout,390,0
EOF

RUN chmod 0644 /home/user/metrics/raw/dashboard_metrics.csv && \
    chmod 755 /home/user

LABEL Author="Observability Task Prep"
LABEL Description="Environment for the 'terse performance summary' assignment with pytest and initial data."