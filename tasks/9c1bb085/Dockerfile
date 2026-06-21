FROM ubuntu:22.04

# Help:
# This container is prepared for the “policy-as-code via crontab” exercise.
# • Python 3 and pytest are installed for automated assessment.
# • A user-space stub of `crontab` is provided so that non-root users can
#   create, list, and remove cron entries without requiring set-uid binaries.

LABEL Author="devsecops-example"

RUN set -e && apt-get update && apt-get install -y --no-install-recommends python3 python3-pip && pip3 install --no-cache-dir pytest && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0777 /home/user

RUN mkdir -p /usr/local/bin && \
cat > /usr/local/bin/crontab << 'EOF'
#!/usr/bin/env bash
# Lightweight, user-space substitute for the system `crontab` utility.
# Stores each user’s crontab in “$HOME/.crontab” and supports the
# minimal option set required for this exercise:  -l  -r  -   <file>

set -e

CRONFILE="${HOME:-/tmp}/.crontab"

usage() {
    echo "Usage: crontab [-l|-r|-] [file]" >&2
    exit 1
}

[[ $# -ge 1 ]] || usage

case "$1" in
    -l)
        if [[ -f "$CRONFILE" ]]; then
            cat "$CRONFILE"
            exit 0
        else
            echo "no crontab for $USER" >&2
            exit 1
        fi
        ;;
    -r)
        rm -f "$CRONFILE"
        exit 0
        ;;
    -)
        # Read new crontab from STDIN
        cat - > "$CRONFILE"
        exit 0
        ;;
    *)
        # Install from file argument
        [[ $# -eq 1 ]] || usage
        [[ -f "$1" ]] || { echo "crontab: file $1 not found" >&2; exit 1; }
        cat "$1" > "$CRONFILE"
        exit 0
        ;;
esac
EOF

RUN chmod 0755 /usr/local/bin/crontab

RUN chmod 755 /home/user

ENV PATH="/usr/local/bin:$PATH"