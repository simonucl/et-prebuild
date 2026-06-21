FROM ubuntu:22.04

# Help / labels from definition file
LABEL Author="Container build script (operations exercise)"
LABEL Description="Sandbox for DNS resolution incident triage task"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

RUN if ! getent group 1000 >/dev/null; then groupadd -g 1000 user; fi && \
    if ! id -u 1000 >/dev/null 2>&1; then useradd -m -u 1000 -g 1000 -s /bin/bash user; fi

RUN mkdir -p /home/user/incidents/tickets && \
    mkdir -p /home/user/resources

RUN cat > /home/user/incidents/tickets/dns_incident_2024.txt <<'EOF'
app.web.internal
example.com
localhost
EOF

RUN cat > /home/user/resources/mock_hosts <<'EOF'
127.0.0.1   localhost
::1         localhost
10.0.0.5    app.web.internal
EOF

RUN cat > /home/user/resources/mock_dns_records.json <<'EOF'
{
  "app.web.internal": { "A": "", "AAAA": "" },
  "example.com":      { "A": "93.184.216.34",
                        "AAAA":"2606:2800:220:1:248:1893:25c8:1946"},
  "localhost":        { "A": "127.0.0.1", "AAAA":"::1" }
}
EOF

RUN chmod 0660 /home/user/incidents/tickets/dns_incident_2024.txt && \
    chmod 0660 /home/user/resources/mock_hosts && \
    chmod 0660 /home/user/resources/mock_dns_records.json && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user

ENV PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/user/.local/bin"