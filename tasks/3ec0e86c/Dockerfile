FROM ubuntu:22.04

# Install Python and pytest for the grading test-suite
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state
RUN mkdir -p /home/user && \
    chmod 0755 /home/user

RUN CONFIG_REPO="/home/user/config_repository" && \
    mkdir -p "$CONFIG_REPO" && \
    chmod 0755 "$CONFIG_REPO"

# Create configuration files
RUN printf "%s\nversion=1.0\nname=alpha\n" > /home/user/config_repository/app_alpha.conf && \
    chmod 0644 /home/user/config_repository/app_alpha.conf

RUN printf "%s\nversion=2.0\nname=alpha\n" > /home/user/config_repository/app_alpha_v2.conf && \
    chmod 0644 /home/user/config_repository/app_alpha_v2.conf

RUN printf "%s\nversion=1.0\nname=beta\n" > /home/user/config_repository/app_beta.conf && \
    chmod 0644 /home/user/config_repository/app_beta.conf

# Ownership
RUN chown -R 0:0 /home/user

# Environment variables
ENV HOME=/home/user
ENV PATH=$PATH:/home/user/.local/bin

# Default run behavior
CMD ["bash"]