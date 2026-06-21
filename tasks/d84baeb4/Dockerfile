FROM ubuntu:22.04

# Environment variables
ENV PYTHONIOENCODING=UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

# Install Python and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create the project directory structure
RUN mkdir -p /home/user/project

# Create translations.yml with the initial English and French blocks only
RUN cat > /home/user/project/translations.yml <<'YAML'
en:
  login: "Login"
  logout: "Logout"

fr:
  login: "Connexion"
  logout: "Déconnexion"
YAML

# Create settings.toml with the initial values
RUN cat > /home/user/project/settings.toml <<'TOML'
[localization]
default_locale = "en_US"
fallback_locale = "en_US"
TOML

# Ensure the user can modify these files later
RUN chmod -R 0777 /home/user

# Labels
LABEL Author="localization-task-setup"
LABEL Description="Container prepared for the localization editing exercise"

# Runscript equivalent
CMD echo "Container for localization exercise. Use this shell to complete the task." && exec /bin/bash