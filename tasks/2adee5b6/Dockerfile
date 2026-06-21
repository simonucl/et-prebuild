FROM ubuntu:22.04

# Basic OS packages
RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip python3-venv zip unzip ca-certificates build-essential

# Upgrade pip and add pytest for the grading harness
RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir pytest

# Prepare project structure under /home/user/dev
RUN mkdir -p /home/user/dev

# 1) Virtual environment
RUN cd /home/user/dev && python3 -m venv .venv_tools

# 2) Install the single required third-party package inside the venv
RUN . /home/user/dev/.venv_tools/bin/activate && \
    pip install --no-cache-dir tqdm==4.66.4 && \
    deactivate

# 3) Create tools directory and output directory
RUN mkdir -p /home/user/dev/tools /home/user/dev/output

# 3) Create the compress.py script
RUN cat > /home/user/dev/tools/compress.py <<'PYEOF'
import sys
import os
import zipfile
from tqdm import tqdm

def main() -> None:
    if len(sys.argv) != 3:
        sys.stderr.write("Usage: python compress.py <input_file> <output_zip>\n")
        sys.exit(1)

    infile, outfile = sys.argv[1], sys.argv[2]

    with zipfile.ZipFile(outfile, "w", zipfile.ZIP_DEFLATED) as zf:
        bar = tqdm(total=1)
        zf.write(infile, arcname=os.path.basename(infile))
        bar.update(1)
        bar.close()

    print(f"Finished: {os.path.abspath(outfile)}")

if __name__ == "__main__":
    main()
PYEOF

RUN chmod 755 /home/user/dev/tools/compress.py

# 4) Sample input file
RUN printf 'Lorem ipsum dolor sit amet.\n' > /home/user/dev/testdata.txt

# 5) Run compress.py once to generate the required archive
RUN /home/user/dev/.venv_tools/bin/python /home/user/dev/tools/compress.py \
    /home/user/dev/testdata.txt /home/user/dev/output/testdata.zip

# 6) Create setup.log with exact required lines (trailing \n included)
RUN cat > /home/user/dev/setup.log <<'LOGEOF'
VENV_SETUP: OK
PACKAGE_TQDM: OK
ZIP_CREATED: OK
LOGEOF

# 7) Ensure non-root users can read/write as tests run unprivileged
RUN chmod -R a+rwX /home/user/dev && \
    chmod 755 /home/user

# Labels
LABEL Author="AI Assistant"
LABEL Description="Utility tools environment with isolated Python venv"

# Help information (as comments):
# This container comes with:
#   • /home/user/dev/.venv_tools  – Python virtual environment (tqdm 4.66.4)
#   • /home/user/dev/tools/compress.py – simple compression utility
#   • /home/user/dev/testdata.txt – sample input
#   • /home/user/dev/output/testdata.zip – pre-built output archive
#   • /home/user/dev/setup.log – status log matching specification