FROM ubuntu:22.04

# Environment variables required by the tests
ENV SEC_KEY=abc123
ENV COMPLIANCE_TOKEN=xyz789
ENV SEC_LEVEL=low

# Update APT index and install Python tooling
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Ensure the expected home directory exists and is writable by non-root users
RUN mkdir -p /home/user \
    && chmod 1777 /home/user

# Make certain no premature compliance artifacts are present
RUN rm -rf /home/user/compliance || true
RUN rm -f /home/user/.bashrc || true

# Set working directory
WORKDIR /home/user

# Set permissions and default command
CMD ["bash", "-c", "chmod 755 /home/user && /bin/bash"]

# Help:
# Base container for the "environment-variable audit" exercise.
# Provides:
#   • Required preset SEC_/COMPLIANCE_ variables
#   • Writable /home/user directory
#   • pytest installed for the grader