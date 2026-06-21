FROM ubuntu:22.04

# Basic tooling
RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create non-privileged demo account and writable HOME
RUN if ! id -u 1000 >/dev/null 2>&1 ; then \
        useradd -m -u 1000 -s /bin/bash user ; \
    fi && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

# Fake crontab implementation
RUN cat <<'EOF' >/usr/local/bin/crontab
#!/usr/bin/env bash
# Minimal shim for the `crontab` command in single-user, daemon-less containers.
set -e
HOME_DIR="${HOME:-/home/user}"
CRON_FILE="${HOME_DIR}/.user_crontab"

case "$1" in
  -l)
      if [[ -f "$CRON_FILE" ]]; then
          cat "$CRON_FILE"
          exit 0
      else
          echo "no crontab for $USER" >&2
          exit 1
      fi
      ;;
  -r)
      rm -f "$CRON_FILE"
      exit 0
      ;;
  -)
      # Read from STDIN
      cat - >"$CRON_FILE"
      exit 0
      ;;
  *)
      if [[ -n "$1" && -f "$1" ]]; then
          cp "$1" "$CRON_FILE"
          exit 0
      fi
      echo "Usage: crontab [-l|-r|FILE|-]" >&2
      exit 1
      ;;
esac
EOF
RUN chmod +x /usr/local/bin/crontab

# Fake systemctl implementation
RUN cat <<'EOF' >/usr/local/bin/systemctl
#!/usr/bin/env bash
# Tiny shim for `systemctl --user` suitable for CI exercises in a container
# that has no real systemd instance.
set -e

# Filter global flags we purposely ignore
user_mode=false
args=()
for a in "$@"; do
    case "$a" in
        --user) user_mode=true ;;
        --all|--no-pager) ;;    # swallow
        *) args+=("$a") ;;
    esac
done

$(! $user_mode) && {
    echo "This shim only supports --user mode." >&2
    exit 0
}

cmd="${args[0]:-}"
shift || true
rest=("${args[@]:1}")

HOME_DIR="${HOME:-/home/user}"
UNIT_DIR="${HOME_DIR}/.config/systemd/user"
STATE_DIR="${HOME_DIR}/.fake_systemd_state"
mkdir -p "${UNIT_DIR}" "${STATE_DIR}"

case "$cmd" in
    daemon-reload)
        # no-op
        exit 0
        ;;
    enable)
        # Accept optional switches such as --now
        units=()
        for x in "${rest[@]}"; do
            case "$x" in
                --now|-f|--force) ;;          # ignored
                *) units+=("$x") ;;
            esac
        done
        for u in "${units[@]}"; do
            echo enabled >"${STATE_DIR}/${u}.enabled"
        done
        exit 0
        ;;
    start|stop|restart)
        # oneshot services: nothing to do
        exit 0
        ;;
    list-timers)
        timers=()
        shopt -s nullglob
        for f in "${STATE_DIR}"/*.enabled; do
            timers+=("$(basename "${f%.enabled}")")
    chmod 755 /home/user

        done
        for f in "${UNIT_DIR}"/*.timer; do
            t="$(basename "$f")"
            [[ " ${timers[*]} " =~ " ${t} " ]] || timers+=("$t")
        done
        for t in "${timers[@]}"; do
            echo "$t"
        done
        exit 0
        ;;
    *)
        # Anything else: succeed silently
        exit 0
        ;;
esac
EOF
RUN chmod +x /usr/local/bin/systemctl

# Environment
ENV PATH=/usr/local/bin:$PATH

# Labels
LABEL Author="ci-cd-task-container"