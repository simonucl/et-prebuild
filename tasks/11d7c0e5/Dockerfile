FROM ubuntu:22.04

# Update package list and install Python + pip
RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 python3-pip locales && \
    rm -rf /var/lib/apt/lists/* && \
    locale-gen en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest

# Create initial project directory structure
RUN install -d -m 0777 /home/user/project-locale/config/locales

# 1. English locale (canonical)
RUN cat > /home/user/project-locale/config/locales/en.yaml <<'EOF'
greeting: "Hello"
farewell: "Goodbye"
login: "Login"
logout: "Logout"
profile: "Profile"
EOF

# 2. Spanish locale (missing two keys)
RUN cat > /home/user/project-locale/config/locales/es.yaml <<'EOF'
greeting: "Hola"
farewell: "Adiós"
login: "Iniciar sesión"
EOF

# 3. French locale (missing three keys)
RUN cat > /home/user/project-locale/config/locales/fr.yaml <<'EOF'
greeting: "Bonjour"
farewell: "Au revoir"
EOF

# 4. build_info.toml with original values
RUN cat > /home/user/project-locale/config/build_info.toml <<'EOF'
version = "1.4.2"
build_number = 17
EOF

# Give non-root users full write access inside the project directory
RUN chmod -R 0777 /home/user/project-locale

# Set environment variables
ENV PATH=/usr/local/bin:/usr/bin:/bin

# Set permissions on /home/user at runtime
RUN chmod 755 /home/user