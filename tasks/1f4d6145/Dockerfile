FROM ubuntu:22.04

# Labels
LABEL Author="Compliance Exercise Image Generator"
LABEL Description="Base image for the \"timezone & locale compliance\" task"

# Help information (as comments):
# This container provides the initial (non-compliant) environment for the
# timezone/locale compliance exercise.  It includes Python and pytest for the
# autograder, plus a writable /home/user with a minimal .bashrc that the
# learner must modify.

# Update package lists and install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        locales

# Install pytest for the grading framework
RUN pip3 install --no-cache-dir pytest

# Generate the en_US.UTF-8 locale so that it is available once the
# student sets LANG later on.
RUN locale-gen en_US.UTF-8

# -----------------------------------------------------------------
# Prepare the initial (non-compliant) user environment
# -----------------------------------------------------------------
# Create the home directory and a minimal .bashrc that does NOT yet
# contain the required export lines.
RUN mkdir -p /home/user

RUN printf '# Default .bashrc for compliance exercise\n' > /home/user/.bashrc

# Relax permissions so the unprivileged student account—whose UID/GID
# is unknown at image-build time—can modify the files as needed.
RUN chmod 777 /home/user && \
    chmod 666 /home/user/.bashrc

# Set working directory
WORKDIR /home/user

# Default command drops the user into a shell
CMD ["/bin/bash"]