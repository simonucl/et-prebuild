FROM ubuntu:22.04

# This image is pre-configured for the localization update task.
# It contains the required initial INI files under /home/user/project/translations
# and has pytest installed for automated evaluation.

LABEL Author="Apptainer Task Preparation"

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project/translations

RUN cat <<'EOF' > /home/user/project/translations/app_en.ini
[General]
welcome=Welcome
exit=Exit

[Errors]
file_not_found=File not found
permission_denied=Permission denied
EOF

RUN cat <<'EOF' > /home/user/project/translations/app_es.ini
[General]
welcome=Bienvenido

[Errors]
file_not_found=Archivo no encontrado
EOF

RUN chmod -R a+rwX /home/user/project

ENV HOME=/home/user