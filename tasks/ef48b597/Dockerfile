FROM ubuntu:22.04

# Help: This container provides the initial state for the Unix text-processing
# assignment.  Two CSV files are pre-installed under
# /home/user/project/translations/, and pytest is available for testing.

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install --no-cache-dir pytest

# Create base directories with write permission for non-root users
RUN mkdir -p /home/user/project/translations && \
    chmod 0777 /home/user && \
    chmod 0777 /home/user/project && \
    chmod 0777 /home/user/project/translations

# Create the en_US.csv file
RUN cat > /home/user/project/translations/en_US.csv <<'EOF'
id,source_en
BTN_OK,OK
BTN_CANCEL,Cancel
MSG_HELLO,Hello
MSG_BYE,Goodbye
LBL_NAME,Name
LBL_EMAIL,Email
ERR_NOTFOUND,Not Found
ERR_ACCESS,Access Denied
EOF

# Create the updates_fr.csv file
RUN cat > /home/user/project/translations/updates_fr.csv <<'EOF'
id,translation_fr
BTN_OK,OK
BTN_CANCEL,Annuler
MSG_HELLO,Bonjour
MSG_BYE,Au revoir
LBL_NAME,Nom
LBL_EMAIL,E-mail
ERR_NOTFOUND,Introuvable
ERR_ACCESS,Accès refusé
EOF

# Ensure readable files and set permissions
RUN chmod 0644 /home/user/project/translations/en_US.csv && \
    chmod 0644 /home/user/project/translations/updates_fr.csv && \
    chmod 755 /home/user

LABEL Author="Automated build for localization task"