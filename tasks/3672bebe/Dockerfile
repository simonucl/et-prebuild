FROM ubuntu:22.04

# Basic tools and Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create workspace
RUN mkdir -p /home/user/translations

# English
RUN cat > /home/user/translations/en.po << 'EOF'
msgid "Hello"
msgstr "Hello"

msgid "Goodbye"
msgstr "Goodbye"

msgid "Yes"
msgstr "Yes"

msgid "No"
msgstr "No"

msgid "Cancel"
msgstr "Cancel"
EOF

# Spanish
RUN cat > /home/user/translations/es.po << 'EOF'
msgid "Hello"
msgstr "Hola"

msgid "Goodbye"
msgstr "Adiós"

msgid "Yes"
msgstr "Sí"

msgid "No"
msgstr "No"

msgid "Cancel"
msgstr ""
EOF

# French
RUN cat > /home/user/translations/fr.po << 'EOF'
msgid "Hello"
msgstr "Bonjour"

msgid "Goodbye"
msgstr ""

msgid "Yes"
msgstr ""

msgid "No"
msgstr ""

msgid "Cancel"
msgstr "Annuler"
EOF

# Ensure read-write permissions
RUN chmod -R a+rwX /home/user

# Labels (note: chmod line in labels section ignored)
LABEL Author="Translation-Exercise-Setup"