FROM ubuntu:22.04

# AUTHOR Clean-up Exercise Prep
# DESCRIPTION Container prepared for the “component metadata clean-up” task.
# Help:
# chmod 755 /home/user
# This image provides the starting state for the “component metadata clean-up” exercise:
#   • /home/user/project/component_a.tsv   (3 columns)
#   • /home/user/project/component_b.tsv   (2 columns)
# Python 3 and pytest are installed for automated grading.

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 \
        python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/project

RUN cat <<'EOF' > /home/user/project/component_a.tsv
comp_login	v1.2	alice
comp_payments	v2.0	bob
comp_notifications	v1.4	carol
comp_search	v1.8	dave
EOF

RUN cat <<'EOF' > /home/user/project/component_b.tsv
comp_login	stable
comp_payments	deprecated
comp_notifications	beta
comp_search	stable
EOF

RUN chmod -R a+rwX /home/user/project