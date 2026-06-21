FROM ubuntu:22.04

# Author myapp-initial-state-preparer
# Description "Container pre-populated with required CI/CD artefacts for myapp"

# This container image provides the exact filesystem state expected by the
# automated tests for the "myapp" project. It also includes Python and pytest.

# Install Python 3, pip and pytest
RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# Create required directory structure
RUN mkdir -p /home/user/releases/myapp/env/development && \
    mkdir -p /home/user/releases/myapp/env/staging && \
    mkdir -p /home/user/releases/myapp/env/production

# Create /home/user/releases/myapp/.env.example
RUN cat > /home/user/releases/myapp/.env.example <<'EOF'
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
API_KEY=
LOG_LEVEL=
EOF

# Create Development .env
RUN cat > /home/user/releases/myapp/env/development/.env <<'EOF'
DB_HOST=localhost
DB_PORT=5432
DB_USER=devuser
DB_PASS=devpass123
API_KEY=DEV-23ab9
LOG_LEVEL=debug
EOF

# Create Staging .env
RUN cat > /home/user/releases/myapp/env/staging/.env <<'EOF'
DB_HOST=staging-db.internal
DB_PORT=5432
DB_USER=stageuser
DB_PASS=stagepass123
API_KEY=STG-584af
LOG_LEVEL=info
EOF

# Create Production .env
RUN cat > /home/user/releases/myapp/env/production/.env <<'EOF'
DB_HOST=prod-db.internal
DB_PORT=5432
DB_USER=produser
DB_PASS=prodpass123
API_KEY=PRD-9f3cd
LOG_LEVEL=warning
EOF

# Create Consolidated CSV
RUN cat > /home/user/releases/myapp/env/all_envs_summary.csv <<'EOF'
ENV,KEY,VALUE
development,DB_HOST,localhost
development,DB_PORT,5432
development,DB_USER,devuser
development,DB_PASS,devpass123
development,API_KEY,DEV-23ab9
development,LOG_LEVEL,debug
staging,DB_HOST,staging-db.internal
staging,DB_PORT,5432
staging,DB_USER,stageuser
staging,DB_PASS,stagepass123
staging,API_KEY,STG-584af
staging,LOG_LEVEL,info
production,DB_HOST,prod-db.internal
production,DB_PORT,5432
production,DB_USER,produser
production,DB_PASS,prodpass123
production,API_KEY,PRD-9f3cd
production,LOG_LEVEL,warning
EOF

# Create Deployment variable log
RUN cat > /home/user/releases/myapp/deploy_vars.log <<'EOF'
[2023-01-01 00:00:00] ENV=staging export DB_HOST=staging-db.internal
[2023-01-01 00:00:00] ENV=staging export DB_PORT=5432
[2023-01-01 00:00:00] ENV=staging export API_KEY=STG-584af
[2023-01-01 00:00:00] ENV=staging export LOG_LEVEL=info
[2023-01-01 00:00:00] ENV=production export DB_HOST=prod-db.internal
[2023-01-01 00:00:00] ENV=production export DB_PORT=5432
[2023-01-01 00:00:00] ENV=production export API_KEY=PRD-9f3cd
[2023-01-01 00:00:00] ENV=production export LOG_LEVEL=warning
EOF

# Set non-root readable permissions
RUN chmod -R 755 /home/user/releases && \
    find /home/user/releases/myapp -type f -exec chmod 644 {} +

RUN chmod 755 /home/user