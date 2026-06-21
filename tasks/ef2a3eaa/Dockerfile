FROM ubuntu:22.04

# Install Python tooling and Pytest
RUN set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create /home/user and set permissions
RUN mkdir -p /home/user && chmod 777 /home/user

# Create project directories
RUN mkdir -p /home/user/projects/portfolio_site/assets && \
    mkdir -p /home/user/projects/portfolio_site/scripts && \
    mkdir -p /home/user/projects/portfolio_site/styles

# Populate source files
RUN printf 'PNGLOGO123\n' > /home/user/projects/portfolio_site/assets/logo.png
RUN printf 'JPGHERO123\n' > /home/user/projects/portfolio_site/assets/hero.jpg
RUN printf "console.log('hi');\n" > /home/user/projects/portfolio_site/scripts/app.js
RUN printf 'body{background:#fff}\n' > /home/user/projects/portfolio_site/styles/style.css

# Permissions
RUN chmod -R 755 /home/user/projects && chmod 755 /home/user

ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=UTF-8

LABEL Author="YourName"
LABEL Description="Environment for timestamped backup procedure task with pytest installed."