#!/data/data/com.termux/files/usr/bin/bash
# openrdp.sh

URL="https://github.com/Dahrulz/RDP/actions/workflows/main.yml"

echo -e "\n🔗  Tekan ENTER untuk buka link di browser..."
read -r

termux-open-url "$URL"
