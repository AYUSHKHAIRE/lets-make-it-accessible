#!/bin/bash

# Update package list and install dependencies
sudo apt-get update
sudo apt-get install -y wget unzip

# Install Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt-get install -y google-chrome-stable

echo "export GOOGLE_CHROME_BIN=/usr/bin/google-chrome" >> ~/.bashrc
source ~/.bashrc
