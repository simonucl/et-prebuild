FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip python3-setuptools && \
    pip3 install --no-cache-dir pytest

# Create non-root user "user" (UID/GID 1000) with home /home/user
RUN if ! getent group 1000 >/dev/null; then \
        groupadd -g 1000 user; \
    fi && \
    if ! id -u 1000 >/dev/null 2>&1; then \
        useradd -m -u 1000 -g 1000 user; \
    fi

# Prepare filesystem layout for the exercise
RUN DASH_ROOT=/home/user/dashboards && \
    STAGING=${DASH_ROOT}/staging && \
    BACKUPS=${DASH_ROOT}/backups && \
    mkdir -p "${STAGING}" "${BACKUPS}" && \
    touch "${BACKUPS}/app_latency.json" \
          "${BACKUPS}/error_rate.json" \
          "${BACKUPS}/infra_overview.json" \
          "${BACKUPS}/business_kpis.json" && \
    echo -n "a" > "${STAGING}/app_latency.json" && \
    touch "${STAGING}/error_rate.json" \
          "${STAGING}/infra_overview.json" \
          "${STAGING}/business_kpis.json"

# Create manifest with expected SHA-256 for empty files
RUN DASH_ROOT=/home/user/dashboards && \
    MANIFEST="${DASH_ROOT}/manifest.sha256" && \
    EMPTY_SHA="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" && \
    printf "%s  app_latency.json\n" "${EMPTY_SHA}" > "${MANIFEST}" && \
    printf "%s  error_rate.json\n" "${EMPTY_SHA}" >> "${MANIFEST}" && \
    printf "%s  infra_overview.json\n" "${EMPTY_SHA}" >> "${MANIFEST}" && \
    printf "%s  business_kpis.json\n" "${EMPTY_SHA}" >> "${MANIFEST}"

# Set permissions: directories 0755, files 0644, owned by the "user" account
RUN DASH_ROOT=/home/user/dashboards && \
    chown -R 1000:1000 /home/user && \
    chmod 755 /home/user && \
    find "${DASH_ROOT}" -type d -exec chmod 0755 {} + && \
    find "${DASH_ROOT}" -type f -exec chmod 0644 {} +

# Labels
LABEL Author="observability-exercise"

# Help information (as comments):
# This container image provides the starting state for the
# "Grafana dashboard integrity" task. It includes:
#   • /home/user/dashboards/staging      – dashboards to be validated
#   • /home/user/dashboards/backups      – pristine copies
#   • /home/user/dashboards/manifest.sha256 – expected checksums
# The file integrity_audit.log is intentionally absent; students must
# create it during the exercise. Pytest is pre-installed for grading.