# Converted from Apptainer: Bootstrap localimage / From ./ubuntu_22.04.sif
FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/dashboards

RUN cat > /home/user/dashboards/prometheus_k8s_legacy.json <<'EOF'
{"title":"Prometheus K8s Legacy","version":1}
EOF

RUN cat > /home/user/dashboards/grafana_overview_legacy.json <<'EOF'
{"title":"Grafana Overview Legacy","version":1}
EOF

RUN cat > /home/user/dashboards/service_latency.json <<'EOF'
{"title":"Service Latency","version":2}
EOF

RUN cat > /home/user/dashboards/readme.md <<'EOF'
These dashboards are managed by the observability team.
EOF

# Permissions
RUN chmod -R 0777 /home/user

# Help text
# chmod 755 /home/user
# This container supplies the starting filesystem state for the
# “dashboard spring-cleaning” task as well as pytest for test execution.

CMD ["/bin/bash"]