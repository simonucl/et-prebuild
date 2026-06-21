FROM ubuntu:22.04

# Install Python and pytest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        gzip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create user home directory
RUN mkdir -p /home/user

# Create initial repository state expected by the tests
RUN mkdir -p /home/user/artifacts/repo_alpha && \
    mkdir -p /home/user/artifacts/repo_beta/module2 && \
    mkdir -p /home/user/artifacts/repo_beta/module3

RUN python3 - << 'PY'
import pathlib

base = pathlib.Path("/home/user/artifacts")
files = [
    base / "repo_alpha" / "file1.bin",
    base / "repo_beta/module2/file2.bin",
    base / "repo_beta/module3/file3.bin",
]

payload = (b"Lorem Ipsum\n") * 100_000  # 1,200,000 bytes

for path in files:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as fh:
        fh.write(payload)
    assert path.stat().st_size == 1_200_000, f"{path} size mismatch"
PY

# Permissions
RUN chmod -R a+rwX /home/user && chmod 755 /home/user

# Environment variables
ENV PYTHONUNBUFFERED=1

# Equivalent to runscript (informational only)
CMD echo "Apptainer container for the artifact optimization task." && exec "$@"