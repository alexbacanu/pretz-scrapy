#!/bin/bash

# Make init_logs directory
mkdir /home/opc/init_logs_update

# --- UPDATE SYSTEM ---
# Update the package list
sudo yum update -y > /home/opc/init_logs_update/yum_update.log

# Upgrade all installed packages to the latest version
sudo yum upgrade -y > /home/opc/init_logs_update/yum_upgrade.log

# Clean up the package manager
sudo yum clean all > /home/opc/init_logs_update/yum_clean.log

# Make scrapy directory
mkdir /home/opc/scrapy

# --- FINAL ---
# Create a notification
echo "Init script finished" > /home/opc/init.log

# Reboot system
sudo reboot