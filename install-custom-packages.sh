# This script installs the custom packages of UPX and 7ZIP because the debian mirrors aren't up to date.
# And aren't consistent between Ubuntu and Debian.

set -e
# Install latest version of 7 zip. (run with sudo)
# refer to https://www.7-zip.org/download.html and get the 64bit linux x86 link for newest version.
# last updated 16-jun-2025
wget https://www.7-zip.org/a/7z2600-linux-x64.tar.xz
# Remove previous install
rm -rf /opt/7z
rm -f /usr/bin/7zzs
# Install to opt and linx to usr bin.
mkdir /opt/7z
tar -xf ./7z2409-linux-x64.tar.xz -C /opt/7z
rm -r ./7z2409-linux-x64.tar.xz
ln -s /opt/7z/7zzs /usr/bin/7zzs

# Install latest version of UPX. (run with sudo)
# refer to https://github.com/upx/upx/releases for updates (amd64_linux.tar version)
# last updated 16-jun-2025
wget -qO- https://github.com/upx/upx/releases/download/v5.1.1/upx-5.1.1-amd64_linux.tar.xz | unxz | tar -x
mv upx-5.1.1-amd64_linux/upx /usr/local/bin
chmod +x /usr/local/bin/upx
rm -r upx-5.1.1-amd64_linux
echo "UPX version $(upx --version)"