FROM ubuntu:22.04

# Author="task-prep"
# Description="Apptainer image with SQLite database and pytest installed for diagnostic snapshot exercise."

RUN set -e && \
    apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3-pip \
        sqlite3 \
        ca-certificates \
        locales && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/app/data

RUN sqlite3 /home/user/app/data/service.db <<'EOF'
CREATE TABLE customers(
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT
);
INSERT INTO customers (id, name, city) VALUES
(1,'Alice','London'),
(2,'Bob','Paris'),
(3,'Charlie','Berlin'),
(4,'Dana','London');

CREATE TABLE orders(
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount REAL
);
INSERT INTO orders (id, customer_id, amount) VALUES
(1,1,100.50),
(2,2,200.00),
(3,1,50.00),
(4,3,75.25);
EOF

RUN chmod -R a+rwX /home/user

CMD chmod 755 /home/user && echo "Diagnostic snapshot container ready. Start an interactive shell."