import os, sys
from rich import print
import subprocess
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent.parent))

from scripts.gen import generate_docker_compose
from scripts.check import check_proxies

def is_sudo():
    if os.geteuid() != 0:
        print("[red][!] This script must be run with root privileges. Please run again with 'sudo'.[/red]")
        sys.exit(1)

def get_running_tor_containers():
    try:
        result = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}}"],
            text=True
        )
        containers = result.splitlines()
        tor_containers = [c for c in containers if c.startswith("tor-")]
        return tor_containers
    except subprocess.CalledProcessError:
        return []
    
def start_tor_service():
    running = get_running_tor_containers()

    if running:
        print(f"[!] Tor service already running ({len(running)} containers)")
        return

    print("[*] Starting Tor proxy service...")
    subprocess.run(["docker", "compose", "up", "-d"], check=True)
    print("[+] Service started successfully")

def stop_tor_containers():
    try:
        result = subprocess.check_output(
            ["docker", "ps", "--format", "{{.Names}}"],
            text=True
        )

        tor_containers = [c for c in result.splitlines() if c.startswith("tor-")]

        if not tor_containers:
            print("[!] No tor containers running")
            return

        print(f"[*] Stopping {len(tor_containers)} tor containers...")
        subprocess.run(["docker", "stop", *tor_containers], check=True)
        print("[+] Tor containers stopped successfully")

    except subprocess.CalledProcessError as e:
        print(f"[!] Error stopping containers: {e}")

def main():
    option = int(input("""
    Select an option:
    [1] Start Tor Proxy Service
    [2] Disable Tor Proxy Service
    [3] Check Tor Proxy Service status
    """))

    if option == 1:
        start_tor_service() # Start the service

    if option == 2:
        stop_tor_containers()

    if option == 3:
        check_proxies()
        



    dependencies()

def dependencies():
    pass

def containers():
    pass


if __name__ == "__main__":
    is_sudo()
    main()