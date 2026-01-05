#!/bin/bash
# Description: Installs the latest stable version of N_m3u8DL-RE.

set -e

echo "Fetching the latest stable release tag for N_m3u8DL-RE..."
LATEST_TAG=$(curl -s https://api.github.com/repos/nilaoda/N_m3u8DL-RE/releases/latest | grep 'tag_name' | cut -d '"' -f4)
echo "Latest N_m3u8DL-RE tag: $LATEST_TAG"

echo "Downloading Linux x64 binary..."
curl -L -o N_m3u8DL-RE.tar.gz "https://github.com/nilaoda/N_m3u8DL-RE/releases/download/$LATEST_TAG/N_m3u8DL-RE_${LATEST_TAG}_linux-x64.tar.gz"

echo "Extracting binary..."
tar -xzf N_m3u8DL-RE.tar.gz
chmod +v +x "N_m3u8DL-RE_${LATEST_TAG}_linux-x64/N_m3u8DL-RE"

echo "Installing to /usr/local/bin..."
sudo mv -v "N_m3u8DL-RE_${LATEST_TAG}_linux-x64/N_m3u8DL-RE" /usr/local/bin/N_m3u8DL-RE

echo "Cleaning up..."
rm N_m3u8DL-RE.tar.gz
rm -rf "N_m3u8DL-RE_${LATEST_TAG}_linux-x64"

echo "Installation complete."
