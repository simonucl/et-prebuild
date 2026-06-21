# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Install Python tools and locale
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales && \
    pip3 install --no-cache-dir pytest && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

# Prepare initial filesystem state
RUN mkdir -p /home/user/conf && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/conf

RUN cat <<'EOF' >/home/user/conf/settings.conf
nombre=José
ciudad=Málaga
clave=paßwörd
EOF

RUN rm -rf /home/user/logs || true

# Apply chmod that was in %environment
RUN chmod 755 /home/user

# Environment variables
ENV LANG=en_US.UTF-8
ENV LC_ALL=en_US.UTF-8
ENV PYTHONIOENCODING=UTF-8

# Default runscript behavior
CMD ["bash"]