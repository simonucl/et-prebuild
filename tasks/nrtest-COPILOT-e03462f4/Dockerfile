FROM python:3.12-slim

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs

# Real Python packaging metadata library (PEP 440 reference implementation).
# Installed at build time so the task is fully solvable with NO network access.
RUN pip install --no-cache-dir "packaging==24.2"

# Unprivileged task user with a stable home directory.
RUN useradd -m -s /bin/bash user

# Stage the read-only task inputs the solver begins from.
COPY work /home/user/work
RUN chown -R user:user /home/user/work

USER user
WORKDIR /home/user
