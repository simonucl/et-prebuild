# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Labels from Apptainer definition
LABEL Author="Apptainer Task Prep"
LABEL Description="Environment for certificate inventory compliance task."

# Update package index and install Python, pip, and dependencies
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    echo "Updating package index and installing Python + pip..." && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
        gnupg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest
RUN --mount=type=cache,target=/root/.cache/pip set -e && \
    echo "Installing pytest for the test-suite..." && \
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Create directory structure and certificate files
RUN set -e && \
    echo "Creating initial directory structure and certificate files..." && \
    mkdir -p /home/user/company_certs && \
    chmod 0777 /home/user

RUN cat > /home/user/company_certs/alpha.crt <<'EOF'
-----BEGIN CERTIFICATE-----
MIIBrzCCAVSgAwIBAgIUBEHPxfN3E3xaQa58aeGeq/QAdzMwCgYIKoZIzj0EAwIw
EzERMA8GA1UEAwwIYWxwaGEuY29tMB4XDTIzMDgwMTAwMDAwMFoXDTI0MDgwMTAw
MDAwMFowEzERMA8GA1UEAwwIYWxwaGEuY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0D
AQcDQgAEi0JPFpKnzGWx/89ZbduCMsZ/HXXIQK5vCk1vZ1tcHTTX3e8DqRL3Ojax
/P6MqxsVXni4eWhv14jArlTc95xJCaNTMFEwHQYDVR0OBBYEFLcdLXx+3CX6XcnG
V7H5PHeTtNKgMB8GA1UdIwQYMBaAFLcdLXx+3CX6XcnGV7H5PHeTtNKgMA8GA1Ud
EwEB/wQFMAMBAf8wCgYIKoZIzj0EAwIDSQAwRgIhAKZDdp2PbgM3N3aR6Vrn956x
BY2NU4VFIfE88ll/aT0cAiEA+2CevulaHYodEc/WWEDuJeayQMZT6X0hgqP/d9vy
q6A=
-----END CERTIFICATE-----
EOF

RUN cat > /home/user/company_certs/bravo.crt <<'EOF'
-----BEGIN CERTIFICATE-----
MIIBqTCCAU+gAwIBAgIUYr2vNhbbX6YsJhBKt3vnDnN/SfAwCgYIKoZIzj0EAwIw
FDESMBAGA1UEAwwJYnJhdm8uY29tMB4XDTIzMDgwMTAwMDAwMFoXDTI0MDgwMTAw
MDAwMFowFDESMBAGA1UEAwwJYnJhdm8uY29tMFkwEwYHKoZIzj0CAQYIKoZIzj0D
AQcDQgAEcJsteUms9UpAJZciV06P88GJEqn3Ejj6inUeJ8V+RaHcRUW2KIiMzFxL
0X58F3RDeo63eVUsVTNff7kwh28zd6NTMFEwHQYDVR0OBBYEFFIqhzyapMI2vlA9
SxrdbidKfnUSMB8GA1UdIwQYMBaAFFIqhzyapMI2vlA9SxrdbidKfnUSMA8GA1Ud
EwEB/wQFMAMBAf8wCgYIKoZIzj0EAwIDRwAwRAIgUoil58x2oyS9MhUlCT3VkOIT
pFmS6r30YIOCQM7DDDeCIHsCIFlfLaHruM3aMcMBXNIN1qNbfXDnpa9eKJeNEqXW
xup6
-----END CERTIFICATE-----
EOF

RUN set -e && \
    chmod 0644 /home/user/company_certs/*.crt && \
    chmod 0755 /home/user/company_certs && \
    echo "Initial state ready."

# Environment setup (from %environment)
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Ensure permissions on home directory
RUN chmod 0755 /home/user

# Help text from Apptainer definition:
# This container provides the initial filesystem and tools required for the
# “certificate inventory” compliance task. Two certificate files are present
# under /home/user/company_certs/. The compliance_logs directory is intentionally
# absent; students/agents must create it and produce the required CSV log.
# Pytest is installed so that the supplied test-suite can be executed within the
# container.