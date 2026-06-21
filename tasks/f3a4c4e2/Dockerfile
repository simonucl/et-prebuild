FROM ubuntu:22.04

# Install Python tooling and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip locales && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir --upgrade pip
RUN python3 -m pip install --no-cache-dir pytest

# Optional: generate UTF-8 locales so that accented characters behave
RUN locale-gen en_US.UTF-8 fr_FR.UTF-8 || true

# Seed localisation repository
RUN mkdir -p /home/user/project/locales

# 1) en_US.csv
RUN cat <<'EOF' > /home/user/project/locales/en_US.csv
KEY,VALUE
greeting,Hello
farewell,Goodbye
ask_name,What is your name?
confirm,Are you sure?
EOF

# 2) fr_FR.csv (initial French translations)
RUN cat <<'EOF' > /home/user/project/locales/fr_FR.csv
KEY,VALUE
greeting,Bonjour
farewell,
ask_name,
confirm,Etes-vous sûr?
EOF

# 3) to_add_fr.txt (new French strings to merge later)
RUN cat <<'EOF' > /home/user/project/locales/to_add_fr.txt
farewell=Au revoir
ask_name=Comment vous appelez-vous?
EOF

# Make sure the student can read/write everything
RUN chmod -R 0777 /home/user/project

RUN chmod 755 /home/user

# Author: Localization-Task-Builder
# Description: Container providing initial state for localisation merge exercise.

# Help:
# This container supplies the exact seed files and directory layout required
# for the localisation merging exercise. Pytest is pre-installed so that the
# automated checker can validate the initial state before the student begins.