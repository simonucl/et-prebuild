FROM ubuntu:22.04

# Labels
LABEL Author="OpenAI ChatGPT"
LABEL Description="Environment for incident triage exercise. Provides initial status.html and installs pytest."

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        curl \
        gnupg \
        build-essential && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user && \
    mkdir -p /home/user/internal_status && \
    chmod 755 /home/user/internal_status && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Place the snapshot HTML file that students must scrape
RUN cat > /home/user/internal_status/status.html <<'EOF'
<!DOCTYPE html>
<html>
<head><title>Internal Status</title></head>
<body>
<h1>Current Incidents</h1>
<table id="incidents">
    <thead>
        <tr><th>ID</th><th>Service</th><th>Severity</th><th>State</th></tr>
    </thead>
    <tbody>
        <tr><td>INC001</td><td>Auth-Service</td><td>High</td><td>Open</td></tr>
        <tr><td>INC002</td><td>Billing-Service</td><td>Critical</td><td>Investigating</td></tr>
        <tr><td>INC003</td><td>Search-Service</td><td>Moderate</td><td>Resolved</td></tr>
        <tr><td>INC004</td><td>Notification-Service</td><td>High</td><td>Monitoring</td></tr>
    </tbody>
</table>
</body>
</html>
EOF

RUN chmod 644 /home/user/internal_status/status.html

WORKDIR /home/user