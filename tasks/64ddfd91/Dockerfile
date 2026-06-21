FROM ubuntu:22.04

# Labels
LABEL Author="Setup for French translation task"

# Install Python and pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    rm -rf /var/lib/apt/lists/*

# Prepare the initial filesystem layout expected by the assignment
RUN mkdir -p /home/user/i18n/source && \
    mkdir -p /home/user/i18n/es

# messages.pot – exact 11-line reference content
RUN cat > /home/user/i18n/source/messages.pot <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"POT-Creation-Date: 2023-01-01 12:00+0000\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Report-Msgid-Bugs-To: \n"
"Language-Team: \n"
"Language: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
EOF

RUN chmod 0644 /home/user/i18n/source/messages.pot

# Placeholder Spanish PO file (content not relevant to tests)
RUN echo '# Spanish translations' > /home/user/i18n/es/messages.po && \
    chmod 0644 /home/user/i18n/es/messages.po

# Ensure French directory and log file do NOT exist yet
RUN rm -rf /home/user/i18n/fr && \
    rm -f /home/user/update_translation.log

# Make top-level directories writable by the (non-root) runtime user
RUN find /home/user -type d -exec chmod 0777 {} +

# Set permissions and environment variables
RUN chmod 755 /home/user

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

WORKDIR /home/user