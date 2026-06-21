# Converted from Apptainer definition file

FROM ubuntu:22.04

# Update apt and install Python + pip
RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user/configs

RUN cat <<'EOF' >/home/user/configs/app.ini
[General]
app_name = SampleApp
version   = 1.2.3

[Security]
encryption  = enabled
allowed_ips = 192.168.1.0/24,10.0.0.0/8

[Compliance]
gdpr  = true
hipaa = false

[Database]
host = db.internal.local
port = 5432
user = appuser
EOF

RUN chmod -R a+rwx /home/user

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

# Labels
LABEL Author="Apptainer Task Builder"
LABEL Description="Container for compliance-audit assignment. Contains initial INI file and pytest."

# Help section as comments
# This container provides the initial environment for the compliance-audit
# programming assignment. It includes:
#   • /home/user/configs/app.ini pre-populated with sample data
#   • pytest installed system-wide
#
# Students are expected to create /home/user/audit/compliance_audit.log
# according to the assignment specification.