FROM ubuntu:22.04

# Install Python, pip and pytest (needed by the assessment harness)
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create initial directory tree and fixture ".policy" files
RUN mkdir -p /home/user/compliance/policies/custom

# data_privacy.policy
RUN cat << 'EOF' > /home/user/compliance/policies/data_privacy.policy
Data Privacy Policy v1
Approved: 2023-07-15
EOF

# incident_response.policy
RUN cat << 'EOF' > /home/user/compliance/policies/incident_response.policy
Incident Response Policy v1
Approved: 2023-07-17
EOF

# network_security.policy
RUN cat << 'EOF' > /home/user/compliance/policies/network_security.policy
Network Security Policy v1
Approved: 2023-07-16
EOF

# custom/third_party.policy
RUN cat << 'EOF' > /home/user/compliance/policies/custom/third_party.policy
Third Party Risk Policy v1
Approved: 2023-07-18
EOF

# Ensure the learner can write under /home/user/compliance
RUN chmod -R 777 /home/user/compliance

# Set permissions on home directory
RUN chmod 755 /home/user

# Labels
LABEL Author="Apptainer Auto-Setup"
LABEL Description="Environment for the Policy Backup exercise (pytest pre-installed)"