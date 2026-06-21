FROM ubuntu:22.04

# Install Python tooling so that the grading harness can run pytest
RUN set -e && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest

# Prepare initial filesystem state expected by the assignment tests
# Create the scripts directory tree
RUN mkdir -p /home/user/cicd/scripts

# Populate the required script files with exact content
RUN printf '#!/usr/bin/env bash\n' > /home/user/cicd/scripts/build.sh && \
    printf 'echo "Running build"\n' >> /home/user/cicd/scripts/build.sh

RUN printf '#!/usr/bin/env bash\n' > /home/user/cicd/scripts/deploy.sh && \
    printf 'echo "Deploying application"\n' >> /home/user/cicd/scripts/deploy.sh

RUN printf '#!/usr/bin/env bash\n' > /home/user/cicd/scripts/test.sh && \
    printf 'echo "Executing tests"\n' >> /home/user/cicd/scripts/test.sh

# Make scripts executable and readable by all users
RUN chmod 0755 /home/user/cicd/scripts/*.sh

# Adjust permissions so the unprivileged runtime user can create
# /home/user/backups later during assessment.
RUN chmod 0777 /home/user && \
    chmod 0755 /home/user/cicd && \
    chmod 0755 /home/user/cicd/scripts

# Ensure Python and shell utilities are on PATH
ENV PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Default action: drop into an interactive shell
CMD ["/bin/bash"]