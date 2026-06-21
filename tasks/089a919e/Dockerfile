FROM ubuntu:22.04

# Labels
LABEL Author="FinOpsTaskBuilder"
LABEL Description="Environment for FinOps permission-handling exercise."

# Help section as comments
# This Docker image provides the starting filesystem layout for the
# FinOps permissions challenge.  Pytest is pre-installed so that the
# automated grader can validate both the initial state and the learner's
# eventual solution.

# Post section
RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 777 /home/user

# Create entrypoint script that sets up the environment at container start
RUN cat <<'EOF' > /usr/local/bin/entrypoint.sh
#!/bin/sh
# This block runs at every container start-up.  It guarantees that the
# FinOps "initial state" required by the exercise exists and is owned by
# the current (unprivileged) user executing the container.

chmod 755 /home/user

CLOUD_DIR="/home/user/cloud_costs"

# Create the base directory if it doesn't exist.
if [ ! -d "${CLOUD_DIR}" ]; then
    mkdir -p "${CLOUD_DIR}"
fi

# Ensure the three raw CSV files are present with the correct content
# and permissions.  They will be created with the UID/GID of the
# runtime user, satisfying the ownership requirement checked by pytest.
for M in Jan Feb Mar; do
    F="${CLOUD_DIR}/raw_costs_${M}.csv"
    if [ ! -f "${F}" ]; then
        printf 'cloud_costs_placeholder\n' > "${F}"
        chmod 644 "${F}"
    fi
done

# Nothing else is created up-front; the learner will take it from here.
export TASK_INITIALIZED=1

exec "$@"
EOF

RUN chmod +x /usr/local/bin/entrypoint.sh

# Environment variables
ENV TASK_INITIALIZED=1

WORKDIR /home/user

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["/bin/bash"]