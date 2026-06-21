# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ---- Installing system packages ----
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        lynx \
        locales \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# ---- Setting up locale ----
RUN locale-gen en_US.UTF-8

# ---- Creating non-root user 'user' ----
RUN useradd -m -u 1000 -s /bin/bash user

# ---- Preparing release_pages directory ----
RUN mkdir -p /home/user/release_pages

# Alpha release page
RUN cat > /home/user/release_pages/alpha_release.html <<'EOF'
<html>
<head><title>Alpha Service Releases</title></head>
<body>
<h1>Alpha Service Releases</h1>

<section class="release">
<h2>v2.3.1</h2>
<p>Date: 2024-07-15</p>
<ul>
<li>FIX: Patched security vulnerability ALP-448</li>
<li>IMPROVEMENT: Reduced memory footprint</li>
</ul>
</section>
</body>
</html>
EOF

# Beta release page
RUN cat > /home/user/release_pages/beta_release.html <<'EOF'
<html>
<head><title>Beta Service Releases</title></head>
<body>
<h1>Beta Service Releases</h1>

<section class="release">
<h2>v1.8.0</h2>
<p>Date: 2024-07-14</p>
<ul>
<li>ADD: GraphQL endpoint for analytics</li>
</ul>
</section>
</body>
</html>
EOF

# Gamma release page
RUN cat > /home/user/release_pages/gamma_release.html <<'EOF'
<html>
<head><title>Gamma Service Releases</title></head>
<body>
<h1>Gamma Service Releases</h1>

<section class="release">
<h2>v5.0.0</h2>
<p>Date: 2024-07-10</p>
<ul>
<li>MAJOR: Migrated to service mesh architecture</li>
</ul>
</section>
</body>
</html>
EOF

# Ensure each file ends with a newline
RUN echo >> /home/user/release_pages/alpha_release.html && \
    echo >> /home/user/release_pages/beta_release.html && \
    echo >> /home/user/release_pages/gamma_release.html

# ---- Setting permissions ----
RUN chmod 755 /home/user/release_pages && \
    chmod 644 /home/user/release_pages/*.html && \
    chown -R user:user /home/user && \
    chmod 755 /home/user

# ---- Installing Python packages ----
RUN --mount=type=cache,target=/root/.cache/pip pip3 install --no-cache-dir pytest

# ---- Environment variables ----
ENV LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8

# %help
# Docker image for release-scraping task with pre-generated HTML release pages.

CMD ["/bin/bash"]