FROM ubuntu:22.04

# Author "Apptainer Build Script"
# Description "Environment for localization synchronisation task with pytest pre-installed."

# This container provides the initial filesystem and dependencies required
# for the localization synchronisation task. pytest is installed so the
# provided tests can be executed inside the container.

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/projects/l10n

# Create /home/user/projects/l10n/en_US.csv (with single trailing newline)
RUN cat <<'EOF' > /home/user/projects/l10n/en_US.csv
key,text
app.title,Weather App
app.greeting,Hello!
error.network,Network error
menu.settings,Settings
menu.quit,Quit
EOF

# Create /home/user/projects/l10n/fr_FR.json (pretty-printed, trailing LF)
RUN cat <<'EOF' > /home/user/projects/l10n/fr_FR.json
{
  "app.title": "Application Météo",
  "menu.settings": "Paramètres"
}
EOF

# Ensure writability for the non-root user who will run inside the container
RUN chmod -R 777 /home/user/projects/l10n && \
    chmod 755 /home/user