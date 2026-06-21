FROM ubuntu:22.04

# Help:
# Container prepared for UTF-16 → UTF-8 repackaging exercise.
# Directories:
#   /home/user/device_configs
#   /home/user/deploy_logs
# Seed file:
#   /home/user/device_configs/config_utf16.txt (UTF-16LE with BOM)
# pytest is pre-installed for grading.

# Update APT and install Python & pip
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip ca-certificates locales && \
    pip3 install --no-cache-dir pytest

# Prepare directory structure
RUN mkdir -p /home/user/device_configs && \
    mkdir -p /home/user/deploy_logs && \
    chmod 700 /home/user/device_configs && \
    chmod 700 /home/user/deploy_logs

# Seed UTF-16LE configuration file (with BOM)
RUN python3 - <<'PY'
import pathlib, os
text = (
    "device_id=alpha123\n"
    "firmware=1.04\n"
    "mode=active\n"
    "# end of file\n"
)
cfg_path = pathlib.Path("/home/user/device_configs/config_utf16.txt")
cfg_path.write_bytes(text.encode("utf-16"))   # utf-16 adds BOM (0xFF 0xFE) automatically
PY

RUN chmod 644 /home/user/device_configs/config_utf16.txt

# Make the owning UID/GID non-root (most graders run as uid 1000)
RUN chown -R 1000:1000 /home/user || true

# Set permissions on home directory
RUN chmod 755 /home/user

LABEL Author="example"