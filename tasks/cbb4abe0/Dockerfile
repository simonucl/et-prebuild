FROM ubuntu:22.04

# Install Python tooling and pytest
RUN set -eu && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip python3-setuptools && \
    pip3 install --no-cache-dir pytest

# Create user home directory
RUN mkdir -p /home/user

# Prepare required directories and files for the QA echo exercise
# 1. Directory
RUN mkdir -p /home/user/qa_echo

# 2. Configuration file: echo.env (exact three lines, newline-terminated)
RUN printf 'ECHO_PORT=9090\nECHO_MODE=testing\nECHO_TIMEOUT=5\n' > /home/user/qa_echo/echo.env

# 3. Bash alias: ensure .bashrc exists and ends with the alias line
RUN printf 'alias echo-test="python3 -m http.server 9090 --directory /home/user/qa_echo"\n' > /home/user/.bashrc

# 4. Verification log: setup.log (exact four-line YAML block)
RUN printf 'setup:\n  config_file: "/home/user/qa_echo/echo.env"\n  bash_alias_added: "yes"\n  status: "ok"\n' > /home/user/qa_echo/setup.log

# Reasonable, readable permissions
RUN chmod 755 /home/user/qa_echo && \
    chmod 644 /home/user/qa_echo/echo.env /home/user/.bashrc /home/user/qa_echo/setup.log