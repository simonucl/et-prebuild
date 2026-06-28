FROM python:3.11-slim

# trsi: pre-create harbor mount points world-writable so non-root-USER envs can be staged
USER root
RUN mkdir -p /solution /tests /logs && chmod 1777 /solution /tests /logs

# bash is required by the validation harness / verifier
RUN apt-get update && apt-get install -y --no-install-recommends bash && \
    rm -rf /var/lib/apt/lists/*

# Create the unprivileged work user and the read-only registry of artifacts.
RUN useradd -m user

WORKDIR /home/user
RUN mkdir -p /home/user/registry/artifacts

# --- Stage the task's STARTING state: a flat pile of artifact files ---------
# File names follow:  <name>@<version>.bin   (name contains no '@').
# Some <version> strings are deliberately NOT valid SemVer 2.0.0 (quarantine).
# Files are empty; only their names matter.
RUN cd /home/user/registry/artifacts && touch \
    'alpha@1.0.0-alpha.bin' \
    'alpha@1.0.0-alpha.1.bin' \
    'alpha@1.0.0-alpha.beta.bin' \
    'alpha@1.0.0-beta.bin' \
    'alpha@1.0.0-beta.2.bin' \
    'alpha@1.0.0-beta.11.bin' \
    'alpha@1.0.0-rc.1.bin' \
    'alpha@1.0.0.bin' \
    'alpha@1.0.bin' \
    'numguard@1.2.9.bin' \
    'numguard@1.2.10.bin' \
    'numguard@1.10.0.bin' \
    'numguard@1.9.0.bin' \
    'numguard@2.0.0.bin' \
    'numguard@v2.0.0.bin' \
    'metabuild@1.0.0+build.2.bin' \
    'metabuild@1.0.0+build.11.bin' \
    'metabuild@1.0.0+build.1.bin' \
    'metabuild@2.0.0.bin' \
    'metabuild@01.0.0.bin' \
    'rconly@0.5.0-rc.1.bin' \
    'rconly@0.5.0-rc.2.bin' \
    'rconly@0.5.0-beta.bin' \
    'rconly@1.0.0-.bin' \
    'junk@1.0.0-alpha..1.bin'

RUN chown -R user:user /home/user/registry

USER user
WORKDIR /home/user
