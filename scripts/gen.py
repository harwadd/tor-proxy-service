# !/usr/bin/env python3
from pathlib import Path

PROXY_COUNT = 3
START_PORT = 25000
ROTATE_SECONDS = 60
GATEWAY_PORT = 8080


def generate_haproxy_cfg():
    cfg = [
        "global",
        "    daemon",
        "    maxconn 256",
        "",
        "defaults",
        "    mode http",
        "    timeout connect 5s",
        "    timeout client  50s",
        "    timeout server  50s",
        "",
        "frontend http_front",
        f"    bind *:{GATEWAY_PORT}",
        "    default_backend tor_back",
        "",
        "backend tor_back",
        "    balance roundrobin",
    ]

    for i in range(PROXY_COUNT):
        cfg.append(f"    server tor{i} tor-{i}:8118 check")

    Path("haproxy.cfg").write_text("\n".join(cfg) + "\n")


def generate_docker_compose():
    TEMPLATE = """  tor-{i}:
    container_name: tor-{i}
    image: dockage/tor-privoxy:latest
    ports:
      - "{port}:8118"
    environment:
      - IP_CHANGE_SECONDS={rotate}
    restart: always
"""

    with open("docker-compose.yml", "w") as f:
        f.write("# Generated automatically\n")
        f.write("services:\n")

        # Tor nodes
        for i in range(PROXY_COUNT):
            f.write(TEMPLATE.format(
                i=i,
                port=START_PORT + i,
                rotate=ROTATE_SECONDS
            ))

        # Gateway
        f.write(f"""
  proxy-gateway:
    image: haproxy:latest
    container_name: tor-gateway
    ports:
      - "{GATEWAY_PORT}:{GATEWAY_PORT}"
    volumes:
      - ./haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg
    restart: always
""")

    print("[+] docker-compose.yml generated")
    generate_haproxy_cfg()
    print("[+] haproxy.cfg generated")


if __name__ == "__main__":
    generate_docker_compose()
