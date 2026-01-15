from config import PROXY_COUNT, PROXY_START_PORT, IP_CHANGE_SECONDS

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
    f.write("# Generated automatically\n\n")
    f.write("version: '3'\n\nservices:\n")

    for i in range(PROXY_COUNT):
        f.write(TEMPLATE.format(i=i, port=PROXY_START_PORT + i, rotate=IP_CHANGE_SECONDS))
