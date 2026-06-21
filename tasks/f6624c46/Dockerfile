FROM ubuntu:22.04

RUN apt-get update -y && apt-get install -y \
        python3 \
        python3-pip \
        diffutils \
        patch \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create the required directory structure
RUN mkdir -p /home/user/dashboards/current && \
    mkdir -p /home/user/dashboards/proposed && \
    mkdir -p /home/user/dashboards/patches && \
    mkdir -p /home/user/dashboards/logs

# Populate the *current* dashboard (old version)
RUN cat > /home/user/dashboards/current/k8s_nodes.json <<'EOF'
{
  "title": "Kubernetes Nodes",
  "panels": [
    {
      "type": "graph",
      "name": "CPU usage",
      "query": "sum(rate(container_cpu_usage_seconds_total[5m])) by (node)"
    },
    {
      "type": "graph",
      "name": "Memory usage",
      "query": "sum(container_memory_usage_bytes) by (node)"
    }
  ],
  "refresh": "5s"
}
EOF

# Populate the *proposed* dashboard (new version, exactly 21 lines)
RUN cat > /home/user/dashboards/proposed/k8s_nodes.json <<'EOF'
{
  "title": "Kubernetes Nodes",
  "panels": [
    {
      "type": "graph",
      "name": "CPU usage",
      "query": "sum(rate(container_cpu_usage_seconds_total[5m])) by (node)"
    },
    {
      "type": "graph",
      "name": "Memory usage",
      "query": "sum(container_memory_usage_bytes) by (node)"
    },
    {
      "type": "graph",
      "name": "Disk usage",
      "query": "sum(container_fs_usage_bytes) by (node)"
    }
  ],
  "refresh": "10s"
}
EOF

# Ensure everything is writable by the non-root runtime user
RUN chmod -R 0777 /home/user/dashboards

ENV HOME=/home/user

# Labels
LABEL Author="observability-task-setup"
LABEL Description="Initial state for dashboard patching exercise"