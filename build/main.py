import os, sys
from rich import print
import pathlib

sys.path.append(str(pathlib.Path(__file__).parent))

def main():
    option = int(input("""
    Select an option:
    [1] Start Tor Proxy Service
    [2] Disable Tor Proxy Service
    [3] Check Tor Proxy Service status
    """))

    if option == 1:
        pass  # Start the service



    dependencies()

def dependencies():
    pass

def containers():
    pass


if __name__ == "__main__":
    main()