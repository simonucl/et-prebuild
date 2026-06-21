FROM ubuntu:22.04

# ------------------------------------------------------------------ #
# Basic tooling                                                      #
# ------------------------------------------------------------------ #
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------ #
# Prepare initial repository state for the exercise                  #
# ------------------------------------------------------------------ #
RUN mkdir -p /home/user/infrastructure-tools/service-monitor

# VERSION file with original version number
RUN printf "1.4.2\n" \
    > /home/user/infrastructure-tools/service-monitor/VERSION

# CHANGELOG.md starting with the 1.4.2 section
RUN cat > /home/user/infrastructure-tools/service-monitor/CHANGELOG.md <<'EOF'
## [1.4.2] - 2023-09-10
### Fixed
- Roll-up of minor Grafana alert regressions (#125)

## [1.4.1] - 2023-08-21
…
EOF

# Pre-existing audit log (can be empty for now)
RUN touch /home/user/version_update.log

# ------------------------------------------------------------------ #
# Relax permissions so the non-root runner inside the container can  #
# modify the files during the exercise                               #
# ------------------------------------------------------------------ #
RUN chmod -R a+rwX /home/user

# Ensure predictable locale
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8