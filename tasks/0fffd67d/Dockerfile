FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer setup for ML data-prep task"

# Update APT and install Python + venv support
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
        python3-pip && \
    # Ensure the latest pip and install pytest for the exercise tests
    python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest && \
    # Create a writable home path expected by the exercise
    mkdir -p /home/user && \
    chmod 0777 /home/user && \
    # Clean up APT cache to keep the image small
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Make sure Python user-installed binaries are on PATH
ENV PATH="/usr/local/bin:/usr/bin:/bin:${PATH}"

WORKDIR /home/user