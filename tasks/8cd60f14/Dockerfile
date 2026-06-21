FROM ubuntu:22.04

# Help section as comments
# Mini ETL Proof-of-Concept
# This is a deliberately *vulnerable* toy ETL pipeline whose transform step
# uses the unsafe `pickle` module. It is meant for security remediation
# exercises only.

RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Create initial vulnerable ETL proof-of-concept in /home/user/etl
RUN mkdir -p /home/user/etl

# extract.py (trivial stub, untouched by the later remediation)
RUN cat > /home/user/etl/extract.py << 'PYCODE'
def extract():
    """
    Dummy extract step that simply returns a constant object.
    """
    return {"fresh": True, "rows": 17}
PYCODE

# load.py (trivial stub, untouched by the later remediation)
RUN cat > /home/user/etl/load.py << 'PYCODE'
def load(data):
    """
    Dummy load step that just prints what it received.
    """
    print("Loading:", data)
PYCODE

# transform.py (INTENTIONALLY VULNERABLE – will be fixed by the learner)
RUN cat > /home/user/etl/transform.py << 'PYCODE'
import pickle
import sys

def transform(path):
    # WARNING: This is deliberately vulnerable!
    with open(path, "rb") as fh:
        data = pickle.load(fh)
    # Identity transform for POC
    return data

if __name__ == "__main__":
    print(transform(sys.argv[1]))
PYCODE

# sample.pkl (pickled representation of {"fresh": True, "rows": 17})
RUN python3 - << 'PY'
import pickle, pathlib, os, json
dst = pathlib.Path("/home/user/etl/sample.pkl")
dst.parent.mkdir(parents=True, exist_ok=True)
with dst.open("wb") as fh:
    pickle.dump({"fresh": True, "rows": 17}, fh)
PY

# README.md (brief project notes)
RUN cat > /home/user/etl/README.md << 'EOF'
# Mini ETL Proof-of-Concept

This is a deliberately *vulnerable* toy ETL pipeline whose transform step
uses the unsafe `pickle` module.  It is meant for security remediation
exercises only.
EOF

# requirements.txt (must start out completely empty)
RUN : > /home/user/etl/requirements.txt

# Ensure every user can read the project files
RUN chmod -R a+rX /home/user/etl

# Set home directory permissions
RUN chmod 755 /home/user

ENV PYTHONUNBUFFERED=1

WORKDIR /home/user

CMD ["sh", "-c", "echo 'Vulnerable ETL environment is ready.' && exec \"$@\"", "--"]