FROM ubuntu:22.04

# Labels
LABEL Author="the-architect"
LABEL Description="Base image for dotenv migration exercise – pytest pre-installed, clean initial state."

# Post installation
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare writable home for the non-root runtime user without
# contaminating the exercise target paths.
RUN mkdir -p /home/user && \
    chmod 0777 /home/user

# Environment variables
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Set working directory
WORKDIR /home/user

# Runscript equivalent
CMD ["sh", "-c", "echo 'Container for dotenv migration exercise.' && echo 'Pytest is available.  Start your work!'"]