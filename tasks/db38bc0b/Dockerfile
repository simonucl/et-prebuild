FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the snapshot directory structure
RUN SNAPSHOT_ROOT="/home/user/compliance_snapshot" && \
    mkdir -p "${SNAPSHOT_ROOT}/etc"

# Create /etc/timezone
RUN echo 'America/New_York' > /home/user/compliance_snapshot/etc/timezone

# Create /etc/locale.conf
RUN echo 'LANG="en_US.UTF-8"' > /home/user/compliance_snapshot/etc/locale.conf && \
    echo 'LC_TIME="en_DK.UTF-8"' >> /home/user/compliance_snapshot/etc/locale.conf

# Create AUDIT_REFERENCE
RUN echo '2024-04-01T12:00:00Z' > /home/user/compliance_snapshot/AUDIT_REFERENCE

# Set permissions so the unprivileged user can read everything
RUN chmod -R a+rX /home/user/compliance_snapshot

# Set permissions on /home/user
RUN chmod 755 /home/user

# This container includes:
# • A pre-populated compliance snapshot under /home/user/compliance_snapshot
#   required for the "time-zone / locale audit" exercise.
# • pytest, installed system-wide, so automated tests can be executed.