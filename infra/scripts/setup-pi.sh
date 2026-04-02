#!/usr/bin/env bash
set -euo pipefail

# Installs Docker Engine + Compose plugin on Raspberry Pi OS (Debian-based).
# Run once on a fresh Pi. Requires sudo.

echo "==> Updating packages..."
sudo apt-get update -qq

echo "==> Installing prerequisites..."
sudo apt-get install -y -qq ca-certificates curl gnupg

echo "==> Adding Docker GPG key..."
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg

echo "==> Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "==> Installing Docker Engine..."
sudo apt-get update -qq
sudo apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "==> Adding current user to docker group..."
sudo usermod -aG docker "$USER"

echo "==> Enabling Docker service..."
sudo systemctl enable docker
sudo systemctl start docker

echo ""
echo "Done! Log out and back in (or reboot) for group changes to take effect."
echo "Then verify with: docker run hello-world"
