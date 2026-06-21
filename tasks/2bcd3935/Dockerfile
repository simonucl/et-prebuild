FROM ubuntu:22.04

RUN set -e && \
    apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends python3-pip && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user/iac

RUN cat > /home/user/iac/main.tf <<'EOF'
resource "aws_security_group" "web" {
  name = "web"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
EOF

RUN cat > /home/user/iac/db.tf <<'EOF'
resource "aws_security_group" "db" {
  name = "db"
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
EOF

RUN : > /home/user/iac/variables.tf

RUN chmod -R a+r /home/user/iac && \
    chmod 0777 /home/user

# From %runscript
RUN chmod 755 /home/user