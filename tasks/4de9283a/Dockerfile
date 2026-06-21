FROM ubuntu:22.04

# Help / labels
LABEL Author="FinOps Exercise Container"
LABEL Description="Base container for the FinOps daily cost report task"

RUN set -eux && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat <<'EOF' >/usr/local/bin/crontab
#!/usr/bin/env bash
# Minimal, non-privileged crontab replacement.
USER_CRONTAB_FILE="${HOME:-/home/user}/.crontab"

if [[ $# -eq 0 ]]; then
    echo "usage: crontab [-l|-r|file|-]" >&2
    exit 1
fi

case "$1" in
    -l)
        if [[ -f "$USER_CRONTAB_FILE" ]]; then
            cat "$USER_CRONTAB_FILE"
            exit 0
        else
            echo "no crontab for $(whoami)" >&2
            exit 1
        fi
        ;;
    -r)
        rm -f "$USER_CRONTAB_FILE"
        exit 0
        ;;
    -)
        # Install crontab from STDIN
        cat > "$USER_CRONTAB_FILE"
        exit 0
        ;;
    *)
        if [[ -f "$1" ]]; then
            cp "$1" "$USER_CRONTAB_FILE"
            exit 0
        else
            echo "crontab: file not found: $1" >&2
            exit 1
        fi
        ;;
esac
EOF

RUN chmod 0755 /usr/local/bin/crontab && chmod 755 /home/user

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH