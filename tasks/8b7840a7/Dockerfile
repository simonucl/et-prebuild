FROM ubuntu:22.04

# Help:
# This container provides the starting filesystem for the “asset build” shell-scripting task.
# Pytest is installed for the evaluation harness.
# The project lives in /home/user/web_project.

RUN set -e && \
    echo "Updating package index and installing Python + pip..." && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest

RUN set -e && \
    echo "Creating project directory structure and source files..." && \
    PROJECT_ROOT="/home/user/web_project" && \
    mkdir -p "${PROJECT_ROOT}/src/css" "${PROJECT_ROOT}/src/js" && \
    printf 'body { background: #fff; }\n' > "${PROJECT_ROOT}/src/css/style1.css" && \
    printf 'h1 { color: #333; }\n'   > "${PROJECT_ROOT}/src/css/style2.css" && \
    printf "console.log('App loaded');\n" > "${PROJECT_ROOT}/src/js/app.js" && \
    printf 'function sum(a,b){return a+b;}\n' > "${PROJECT_ROOT}/src/js/utils.js" && \
    printf '<!DOCTYPE html><html><head><title>Home</title></head><body><h1>Home</h1></body></html>\n'  > "${PROJECT_ROOT}/src/index.html" && \
    printf '<!DOCTYPE html><html><head><title>About</title></head><body><h1>About</h1></body></html>\n' > "${PROJECT_ROOT}/src/about.html" && \
    rm -rf "${PROJECT_ROOT}/dist" || true && \
    rm -f  "${PROJECT_ROOT}/build_assets.sh" || true && \
    chmod -R a+rwX "${PROJECT_ROOT}"

RUN chmod 755 /home/user

LABEL Author="task-generator"
LABEL Description="Initial state for web_project asset build automation task"