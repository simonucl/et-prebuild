FROM ubuntu:22.04

# Labels
LABEL Author="Release Manager Exercise Container"

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        make \
        tar \
        gzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the test harness
RUN pip3 install --no-cache-dir pytest

# Prepare initial workspace expected by the exercise
RUN mkdir -p /home/user/release/app

# VERSION file with exact content "1.0.0\n"
RUN printf '1.0.0\n' > /home/user/release/VERSION

# Placeholder application source
RUN printf 'print("Hello, World!")\n' > /home/user/release/app/main.py

# Adjust permissions so that the non-root runtime user can modify files
RUN chmod -R a+rX /home/user && \
    chmod -R a+w /home/user/release && \
    chmod 755 /home/user

# Ensure standard paths are available
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

WORKDIR /home/user