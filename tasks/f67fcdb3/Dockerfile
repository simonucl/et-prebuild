FROM ubuntu:22.04

# Update package list and install Python + pip
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip

# Install pytest for the automated tests
RUN pip3 install --no-cache-dir pytest

# Set up the initial project directory structure and CSV file
RUN mkdir -p /home/user/project/localization

RUN cat > /home/user/project/localization/translations.csv <<'EOF'
key,en,fr,de
WELCOME,Welcome,,Willkommen
EXIT,Exit,Quitter,Beenden
SAVE,Save,Enregistrer,Speichern
CANCEL,Cancel,Annuler,Abbrechen
DELETE,Delete,Supprimer,Löschen
EOF

# Ensure the agent (non-root user) can modify the files and directory
RUN chmod -R 0777 /home/user/project

# Set environment variables
ENV LC_ALL=C.UTF-8

# Set permissions on home directory at runtime
RUN chmod 755 /home/user