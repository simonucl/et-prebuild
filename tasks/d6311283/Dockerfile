FROM ubuntu:22.04

# Update OS and install required packages
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gettext \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install pytest for the grader
RUN pip3 install --no-cache-dir pytest

# Create initial directory structure and seed files for the exercise
RUN mkdir -p /home/user/projects/website/locale/fr/LC_MESSAGES && \
    mkdir -p /home/user/projects/website/logs && \
    mkdir -p /home/user/resources

# messages.po (untranslated)
RUN cat > /home/user/projects/website/locale/fr/LC_MESSAGES/messages.po <<'EOF'
msgid ""
msgstr ""
"Project-Id-Version: website 1.4\n"
"Language: fr\n"
"Content-Type: text/plain; charset=UTF-8\n"

#: src/errors.c:45
msgid "Server unreachable"
msgstr ""
EOF

# DNS seed file
RUN cat > /home/user/resources/dns_seed.txt <<'EOF'
staging.l10n.test 203.0.113.30
api.l10n.test     203.0.113.31
EOF

# Ensure permissions allow the non-root runtime user to work
RUN chmod -R a+rwx /home/user

# Environment variables
ENV PATH=/usr/local/bin:$PATH