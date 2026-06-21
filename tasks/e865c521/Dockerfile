FROM ubuntu:22.04

# Install required packages
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        git \
        python3-pip \
        ca-certificates && \
    pip3 install --no-cache-dir pytest

# Create initial project layout expected by the exercise
RUN mkdir -p /home/user/projects/optimize_app

WORKDIR /home/user/projects/optimize_app

# Initialise an empty Git repository
RUN git init

# Baseline solver_config.yaml (must match tests EXACTLY, incl. newline)
RUN cat > solver_config.yaml <<'EOF'
solver:
  name: "glpk"
  tolerance: 1e-6
  max_iterations: 1000
  verbose: false
EOF

# Initial commit
RUN git config --local user.name "Builder" && \
    git config --local user.email "builder@example.com" && \
    git add solver_config.yaml && \
    git commit -m "chore: initial GLPK config"

# Ensure the runtime (non-root) user can freely modify the workspace
RUN chmod -R a+rwx /home/user

LABEL Author="optimization-setup-bot"
LABEL Description="Base image for optimise_app exercise – contains initial Git repository"

# Help: This container sets up the starting state for the "optimise_app" exercise.
# A Git repository is prepared in /home/user/projects/optimize_app with a
# baseline solver_config.yaml. Pytest is installed for running the automated
# checks.