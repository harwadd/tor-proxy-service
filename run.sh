#!/bin/bash
set -e

echo "[*] Starting the build process..."

spinner() {
  local pid=$1
  local spin='-\|/'

  while kill -0 "$pid" 2>/dev/null; do
    for i in 0 1 2 3; do
      printf "\b%s" "${spin:$i:1}"
      sleep 0.1
    done
  done

  printf "\b ✓\n"
}


# Check for Python3
if ! command -v python3 >/dev/null 2>&1; then
  echo "[!] Python3 is not installed."
  exit 1
fi

# Create venv
printf "[+] Creating virtual environment... "
python3 -m venv venv > /dev/null 2>&1 &
spinner $!

# Activate venv
echo "[+] Activating virtual environment..."
source venv/bin/activate

# Install deps
printf "[+] Installing dependencies... "
pip install -r requirements.txt > /dev/null 2>&1 &
spinner $!

echo "[✓] Build completed successfully."

# Run the application
printf "[*] Run the application now? (y/n): "
read -r run_now
if [[ "$run_now" == "y" || "$run_now" == "Y" ]]; then
  printf "[*] Starting the application...\n"
  sudo python3 build/main.py
else
  echo "[*] You can start the application later running 'sudo python3 build/main.py'."
fi