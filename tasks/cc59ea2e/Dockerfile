FROM ubuntu:22.04

# Set environment variables
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN set -eux && \
    # Update package index and install Python tooling
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    # Install pytest for the automated grading suite
    pip3 install --no-cache-dir pytest

# Create the incidents directory with strict permissions
RUN mkdir -p /home/user/incidents && \
    chmod 700 /home/user/incidents

# Payload files (exact byte content, NO trailing newline)
RUN printf 'test' > /home/user/incidents/update1.txt && \
    printf 'abc' > /home/user/incidents/update2.txt

# Vendor-supplied SHA-256 sidecar files (each ends with exactly one NL)
RUN printf '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  update1.txt\n' \
        > /home/user/incidents/update1.txt.sha256 && \
    printf '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08  update2.txt\n' \
        > /home/user/incidents/update2.txt.sha256

# Ensure ownership is root:root and set home directory permissions
RUN chown -R root:root /home/user/incidents && \
    chmod 755 /home/user

# Default command
CMD ["sh", "-c", "echo 'Docker image for checksum verification task.' && echo 'Invoke your solution scripts or open a shell as needed.'"]