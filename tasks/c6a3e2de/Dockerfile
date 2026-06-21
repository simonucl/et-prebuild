# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# Help / labels
# Author="ChatGPT"
# Description="Apptainer image for the container-ops workflow task with pytest pre-installed."

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked --mount=type=cache,target=/var/lib/apt,sharing=locked --mount=type=cache,target=/root/.cache/pip set -e && \
    apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip curl && \
    pip3 install --no-cache-dir pytest && \
    mkdir -p /home/user && \
    chmod 0777 /home/user

RUN cat > /usr/local/bin/docker << 'PYEOF'
#!/usr/bin/env python3
import sys, os, json, subprocess, random, string, signal

DATA_DIR = "/tmp/fake_docker"
IMAGES_F = os.path.join(DATA_DIR, "images.json")
CONTS_F  = os.path.join(DATA_DIR, "containers.json")

def _load(path):
    try:
        with open(path) as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def _save(path, data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(path, "w") as fh:
        json.dump(data, fh)

images     = _load(IMAGES_F)
containers = _load(CONTS_F)

def _rand_id():
    return ''.join(random.choices('0123456789abcdef', k=64))

def cmd_image(args):
    if len(args) >= 2 and args[0] == "inspect":
        tag = args[1]
        if tag in images:
            print(json.dumps([{"Id": images[tag]}]))
            return 0
        return 1
    print("docker: unknown image command", file=sys.stderr)
    return 1

def cmd_build(args):
    tag = None
    for i, a in enumerate(args):
        if a in ("-t", "--tag") and i + 1 < len(args):
            tag = args[i + 1]
            break
        if a.startswith("-t"):
            tag = a[2:]
            break
        if a.startswith("--tag="):
            tag = a.split("=", 1)[1]
            break
    if not tag:
        print("docker: missing -t/--tag on build", file=sys.stderr)
        return 1
    img_id = _rand_id()
    images[tag] = img_id
    print(f"Successfully built {img_id[:12]}")
    print(f"Successfully tagged {tag}")
    _save(IMAGES_F, images)
    return 0

def cmd_run(args):
    detached = False
    name     = None
    hostport = "8088"
    image    = None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-d", "--detach"):
            detached = True
        elif a in ("--name",):
            name = args[i + 1]; i += 1
        elif a in ("-p", "--publish"):
            hp = args[i + 1]; i += 1
            hostport = hp.split(":")[0]
        elif a.startswith("-p"):
            hostport = a[2:].split(":")[0]
        i += 1
    if args:
        image = args[-1]
    if image not in images:
        print(f"docker: image {image} not found", file=sys.stderr)
        return 1
    if not name:
        name = "ctr_" + _rand_id()[:12]
    serve_dir = "/home/user/container_work" if os.path.isdir("/home/user/container_work") else "."
    idx = os.path.join(serve_dir, "index.html")
    if not os.path.exists(idx):
        with open(idx, "w") as fh:
            fh.write("Hello from Container Ops!\n")
    proc = subprocess.Popen(
        ["python3", "-m", "http.server", hostport,
         "--bind", "127.0.0.1", "--directory", serve_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    cid = _rand_id()
    containers[name] = {"Id": cid, "Pid": proc.pid, "Status": "running"}
    _save(CONTS_F, containers)
    print(cid)
    return 0

def _ps_output(show_all, quiet, fmt, name_filter):
    out = []
    for n, info in containers.items():
        if not show_all and info["Status"] != "running":
            continue
        if name_filter and name_filter not in n:
            continue
        if quiet:
            out.append(info["Id"][:12])
        elif fmt:
            line = fmt.replace("{{.ID}}", info["Id"][:12]).replace("{{.Names}}", n)
            out.append(line)
        else:
            out.append(f"{info['Id'][:12]}\t{n}\t{info['Status']}")
    return "\n".join(out)

def cmd_ps(args):
    show_all = False
    quiet    = False
    fmt      = None
    name_fil = None
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-a", "--all"):
            show_all = True
        elif a == "-q":
            quiet = True
        elif a == "--format":
            fmt = args[i + 1]; i += 1
        elif a == "--filter":
            fil = args[i + 1]; i += 1
            if fil.startswith("name="):
                name_fil = fil.split("=", 1)[1]
        i += 1
    print(_ps_output(show_all, quiet, fmt, name_fil))
    return 0

def cmd_stop(args):
    for name in args:
        info = containers.get(name)
        if info and info["Status"] == "running":
            try:
                os.kill(info["Pid"], signal.SIGTERM)
            except ProcessLookupError:
                pass
            info["Status"] = "exited"
    _save(CONTS_F, containers)
    return 0

def cmd_rm(args):
    for name in args:
        info = containers.pop(name, None)
        if info:
            try:
                os.kill(info["Pid"], signal.SIGKILL)
            except Exception:
                pass
    _save(CONTS_F, containers)
    return 0

def main():
    if len(sys.argv) < 2:
        print("docker: missing command", file=sys.stderr)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    rc = 1
    if cmd == "image":
        rc = cmd_image(args)
    elif cmd == "build":
        rc = cmd_build(args)
    elif cmd == "run":
        rc = cmd_run(args)
    elif cmd == "ps":
        rc = cmd_ps(args)
    elif cmd == "stop":
        rc = cmd_stop(args)
    elif cmd == "rm":
        rc = cmd_rm(args)
    elif cmd == "--version":
        print("Fake Docker version 20.10.0")
        rc = 0
    else:
        print(f"docker: unknown command {cmd}", file=sys.stderr)
    sys.exit(rc)

if __name__ == "__main__":
    main()
PYEOF

RUN chmod +x /usr/local/bin/docker

ENV PATH=/usr/local/bin:/usr/bin:/bin:$PATH
ENV HOME=/home/user

RUN chmod 755 /home/user