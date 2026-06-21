FROM ubuntu:22.04

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN mkdir -p /home/user/project/i18n

RUN cat <<'JSON_EOF' > /home/user/project/i18n/fr.json
{
  "CancelButton": "Annuler",
  "AddButton": "Ajouter",
  "DeleteDialogTitle": "Supprimer l’élément ?",
  "EditLabel": "Modifier",
  "SaveSuccess": "Enregistré avec succès"
}
JSON_EOF

RUN chmod 777 /home/user/project /home/user/project/i18n && \
    chmod 666 /home/user/project/i18n/fr.json

RUN mkdir -p /home/user && chmod 755 /home/user