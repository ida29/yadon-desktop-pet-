#!/bin/bash

# Yadon Desktop Pet Auto-start Installation Script

echo "ヤドンペット自動起動設定をインストールします..."

# Create LaunchAgents directory if it doesn't exist
mkdir -p ~/Library/LaunchAgents

# Copy plist file to LaunchAgents directory
cp com.yadon.pet.plist ~/Library/LaunchAgents/

# Load the LaunchAgent
launchctl load ~/Library/LaunchAgents/com.yadon.pet.plist

echo "インストール完了！PCを再起動すると自動的にヤドンが起動します。"
echo ""
echo "手動で起動するには："
echo "  python3 yadon_pet.py"
echo ""
echo "自動起動を無効にするには："
echo "  launchctl unload ~/Library/LaunchAgents/com.yadon.pet.plist"
echo ""
echo "完全にアンインストールするには："
echo "  launchctl unload ~/Library/LaunchAgents/com.yadon.pet.plist"
echo "  rm ~/Library/LaunchAgents/com.yadon.pet.plist"