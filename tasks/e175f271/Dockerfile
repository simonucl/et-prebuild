FROM ubuntu:22.04

# Labels
LABEL Author="AI-Generated"
LABEL Description="Container for the \"Acme Cost Optimizer\" FinOps task – initial state pre-configured."

# Help information as comments
# This container sets up the initial workspace for the Acme Cost Optimizer
# exercise.  It installs Python 3, pytest, and seeds the project directory
# at /home/user/acme-cost-optimizer/ with the required files in their
# initial state.

RUN set -e && \
    apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        ca-certificates \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest

# Prepare initial project layout expected by the grader
RUN mkdir -p /home/user/acme-cost-optimizer

# version.txt – must contain exactly "2.5.4" with a single trailing newline
RUN printf '2.5.4\n' > /home/user/acme-cost-optimizer/version.txt

# CHANGELOG.md – initial content as described in the specification
RUN cat > /home/user/acme-cost-optimizer/CHANGELOG.md <<'EOF'
## [2.5.4] - 2024-03-28
### Fixed
- Corrected amortised reservation cost maths.

## [2.5.3] - 2024-03-10
### Added
- Introduced forecast accuracy metric.

EOF

# Ensure the future non-root user can modify the project files
RUN chmod -R a+rwX /home/user

# Environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

WORKDIR /home/user