#!/bin/bash

# --- UPDATE SYSTEM ---
cd /home/${ssh_user}/

# Update the package list
sudo yum update -y

# Upgrade all installed packages to the latest version
sudo yum upgrade -y

# Install redis
sudo yum install redis -y

# Make scrapy directory
mkdir -p scrapy

# --- FINAL ---
# Clean up the package manager
sudo yum clean all

# Create a notification
echo "Cloud-Init script finished" > init.log

# Reboot system
sudo reboot