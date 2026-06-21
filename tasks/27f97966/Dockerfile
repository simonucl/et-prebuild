FROM ubuntu:22.04

# Author ComplianceFixtureBot
# Description "Sets up initial filesystem state for PCI-DSS audit task with pytest pre-installed."

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/compliance/2021/archive && \
    mkdir -p /home/user/compliance/2022 && \
    mkdir -p /home/user/compliance/2023/draft

RUN cat > /home/user/compliance/2021/payments_policy.txt <<'EOF'
Payments Processing Policy
Revision: 2021-03-15

All cardholder data is handled in accordance with PCI-DSS v3.2.
We mandate quarterly scans to satisfy PCI-DSS requirements.
End of document.
EOF

RUN cat > /home/user/compliance/2021/archive/old_payment.md <<'EOF'
Legacy system documentation referencing PCI-DSS.
EOF

RUN cat > /home/user/compliance/2022/network_controls.md <<'EOF'
# Network Security Controls
The firewall configuration complies with PCI-DSS guidelines.
Traffic is segmented based on PCI-DSS zones.
EOF

RUN cat > /home/user/compliance/2022/README.txt <<'EOF'
This directory contains network control documentation.
EOF

RUN cat > /home/user/compliance/2023/draft/pci_overview.md <<'EOF'
# PCI Overview Draft
PCI-DSS scope determination is critical.
PCI-DSS scope includes all systems that store, process, or transmit cardholder data.
PCI-DSS!
EOF

RUN chmod -R 755 /home/user/compliance && \
    find /home/user/compliance -type f -exec chmod 644 {} \;

RUN chmod 755 /home/user

RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# This container image provides the initial filesystem fixtures and
# pytest dependency required for the “PCI-DSS audit trail” task.
# Students will run their solutions inside this environment.