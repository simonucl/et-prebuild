FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer Task Prep Bot"
LABEL Description="Base image for tz/locale diagnostics exercise with pytest pre-installed"

# ------------------------------------------------------------------
# Basic non-interactive apt configuration (avoid tzdata prompts)
# ------------------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive

# Update package index and install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-pip \
        python3-setuptools \
        locales \
        tzdata

# ------------------------------------------------------------------
# Python testing framework
# ------------------------------------------------------------------
RUN pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Ensure the reference time-zone file is exactly as expected
# ------------------------------------------------------------------
RUN echo "Etc/UTC" > /etc/timezone

# ------------------------------------------------------------------
# Generate the en_US.UTF-8 locale that the learner will need
# ------------------------------------------------------------------
RUN sed -i 's/^# *\(en_US.UTF-8 UTF-8\)/\1/' /etc/locale.gen && \
    locale-gen en_US.UTF-8

# ------------------------------------------------------------------
# Create an unprivileged user that the grader & learner will use
# ------------------------------------------------------------------
RUN if ! id -u user >/dev/null 2>&1; then \
        groupadd -g 1000 user && \
        useradd -m -u 1000 -g 1000 -s /bin/bash user; \
    fi

# Clean up APT caches to keep the image small
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set permissions on home directory
RUN chmod 755 /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Default command
CMD ["/bin/bash"]