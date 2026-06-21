FROM ubuntu:22.04

# Update package lists and install Python tooling
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip

# Install pytest for the test suites
RUN pip3 install --no-cache-dir pytest

# Prepare the initial filesystem state
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Create initial outline file
RUN printf '# System Architecture\nInitial outline.\n' > /home/user/architecture_outline.md && \
    chmod 0644 /home/user/architecture_outline.md

# Apply environment-time permissions change from %environment
RUN chmod 755 /home/user

# Environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Default runscript behavior
CMD ["bash", "-l"]