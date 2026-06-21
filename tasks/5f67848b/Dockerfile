# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# ------------------------------------------------------------------
# Update package lists and install Python tooling
# ------------------------------------------------------------------
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip && \
    pip3 install --no-cache-dir pytest

# ------------------------------------------------------------------
# Prepare the initial state required for the grading tests
# ------------------------------------------------------------------
# Create the user home and build log directory structure
RUN mkdir -p /home/user/build_logs && \
    chmod 0777 /home/user /home/user/build_logs

# Populate the canonical Gradle build log
RUN cat <<'EOF' > /home/user/build_logs/gradle_build.log
Task :app:compileDebugJava FAILED
Task :app:compileDebugResources
Task :lib:compileDebugKotlin FAILED
Task :lib:processDebugResources
Task :network:compileReleaseJava
Task :app:assembleDebug FAILED
BUILD FAILED in 1m 46s
7 actionable tasks: 7 executed
EOF

# Ensure the log file is readable by everyone and modifiable by the runtime user if needed
RUN chmod 0666 /home/user/build_logs/gradle_build.log

# Clean up apt caches to keep the image small
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# ------------------------------------------------------------------
# Environment configuration
# ------------------------------------------------------------------
ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH

# Match the intended home directory permissions from the Apptainer environment
RUN chmod 755 /home/user

# ------------------------------------------------------------------
# Help / runscript equivalent
# Container for Gradle failure dashboard challenge.
# Execute your solution script separately.
# ------------------------------------------------------------------