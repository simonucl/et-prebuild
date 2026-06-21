FROM ubuntu:22.04

# Labels
LABEL Author="localization-task-preparer"
LABEL Description="Container for localization log-filtering task – initial state with source log and pytest installed."

# Update apt repositories and install Python and pip
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip

# Install pytest for the assessment harness
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir pytest

# Create the initial project directory structure
RUN mkdir -p /home/user/project/logs

# Populate the source log file with the exact required contents
RUN cat > /home/user/project/logs/update_2023-04-01.log <<'EOF'
[INFO]  I1000: Assets scanned: 42
[ERROR] E2300: Missing translation for locale 'fr' key 'home.title'
[ERROR] E2300: Missing translation for locale 'de' key 'settings.label'
[ERROR] E2300: Missing translation for locale 'es' key 'about.header'
[WARN]  W3400: Placeholder count mismatch in 'de' for key 'login.button'
[WARN]  W3400: Placeholder count mismatch in 'fr' for key 'profile.subtitle'
[INFO]  I1001: Catalog compiled
[ERROR] E2300: Missing translation for locale 'fr' key 'logout.confirm'
[WARN]  W3400: Placeholder count mismatch in 'it' for key 'cart.total'
[INFO]  I1002: Build complete
[ERROR] E2300: Missing translation for locale 'de' key 'contact.phone'
[WARN]  W3400: Placeholder count mismatch in 'de' for key 'order.summary'
[ERROR] E2300: Missing translation for locale 'fr' key 'checkout.button'
[ERROR] E2300: Missing translation for locale 'de' key 'error.404'
[INFO]  Summary: 6 missing translations, 4 warnings, 2 infos
EOF

# Ensure the directories are writable by the (non-root) runtime user
RUN chmod -R 0777 /home/user

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH