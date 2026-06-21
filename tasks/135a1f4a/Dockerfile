FROM ubuntu:22.04

ENV PYTHONIOENCODING="utf-8"
ENV LC_ALL="C.UTF-8"

RUN set -e && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        python3-setuptools \
        python3-wheel && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir pytest tomli

RUN python3 - <<'PY'
import site, pathlib, textwrap
try:
    import tomllib  # noqa: F401
except ModuleNotFoundError:
    lib_dir = site.getsitepackages()[0]
    stub = pathlib.Path(lib_dir) / "tomllib.py"
    if not stub.exists():
        stub.write_text(textwrap.dedent("""
        \"\"\"Compatibility wrapper mapping tomllib to tomli for Python < 3.11.\"\"\"
        import io as _io
        import tomli as _tomli

        def loads(s, /, *, parse_float=float):
            return _tomli.loads(s, parse_float=parse_float)

        def load(fp, /, *, parse_float=float):
            data = fp.read()
            if isinstance(data, bytes):
                data = data.decode()
            return _tomli.loads(data, parse_float=parse_float)
        """))
PY

RUN mkdir -p /home/user/app_config

RUN cat <<'EOF' > /home/user/app_config/config.yaml
server:
  host: "0.0.0.0"
  port: 8080

logging:
  level: "INFO"
  format: "json"
EOF

RUN cat <<'EOF' > /home/user/app_config/logging.toml
[output.console]
enabled = true
level = "INFO"

[output.file]
enabled = false
path = "/var/log/app/service.log"
level = "INFO"
rotation = "daily"
EOF

RUN chmod -R a+rX /home/user && chmod 755 /home/user