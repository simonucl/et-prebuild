FROM ubuntu:22.04

# Labels
LABEL Author="Apptainer task setup"
LABEL Description="Container with initial CSV data for product processing task"

RUN set -eux && \
    apt-get update -y && \
    apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/data/raw && \
    mkdir -p /home/user/data/combined && \
    mkdir -p /home/user/data/processed

# products_2021.csv
RUN cat > /home/user/data/raw/products_2021.csv <<'EOF'
id,product_name,price,category,discontinued
1,Widget,19.99,gadgets,no
2,Gizmo,29.99,gadgets,no
3,OldThing,9.99,antiques,yes
EOF

# products_2022.csv
RUN cat > /home/user/data/raw/products_2022.csv <<'EOF'
id,product_name,price,category,discontinued
4,Widget Pro,24.99,gadgets,no
5,Gizmo Plus,34.99,gadgets,no
6,AncientThing,49.99,antiques,no
EOF

# Ensure the future working directories are writable by the
# unprivileged user who will run inside the container.
RUN chmod -R a+rwX /home/user

ENV HOME=/home/user

WORKDIR /home/user