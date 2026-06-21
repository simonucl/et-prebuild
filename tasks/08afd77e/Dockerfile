FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Prepare initial dataset - Directory structure
RUN mkdir -p /home/user/data/raw && \
    chmod 755 /home/user && \
    chmod 755 /home/user/data && \
    chmod 755 /home/user/data/raw

# Create the Windows-1252–encoded CSV file exactly as specified
RUN python3 - <<'PY'
import os, pathlib

content = (
    "id,name,city\n"
    "1,José,Montréal\n"
    "2,Léa,Berlin\n"
    "3,O'Connor,Dublin\n"
)

path = pathlib.Path("/home/user/data/raw/customers_win1252.csv")
path.write_bytes(content.encode("cp1252"))
os.chmod(path, 0o644)
PY

# Labels
LABEL Author="encoding-conversion setup"

# Help: Container pre-configured for the "encoding-conversion" exercise.
# Includes pytest and the initial Windows-1252 CSV dataset under
# /home/user/data/raw.