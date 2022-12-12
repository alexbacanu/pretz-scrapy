#!/bin/bash

# Make logs directory
mkdir -p /home/opc/init_logs_update
mkdir -p /home/opc/init_logs_mongodb

# --- UPDATE SYSTEM ---
# Update the package list
sudo yum update -y > /home/opc/init_logs_update/yum_update.log

# Upgrade all installed packages to the latest version
sudo yum upgrade -y > /home/opc/init_logs_update/yum_upgrade.log

# --- ADD MONGODB ---
# Add the MongoDB repository
repo="[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/\$releasever/mongodb-org/6.0/aarch64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc"

sudo echo "$repo" > /etc/yum.repos.d/mongodb-org-6.0.repo

# Update the package index
sudo yum update -y > /home/opc/init_logs_mongodb/yum_update.log

# Install MongoDB
sudo yum install -y mongodb-org > /home/opc/init_logs_mongodb/yum_install.log

# Start the MongoDB service
# sudo systemctl start mongod > /home/opc/init_logs_mongodb/systemctl_start.log

# Enable the MongoDB service to start automatically on boot
# sudo systemctl enable mongod > /home/opc/init_logs_mongodb/systemctl_enable.log

# Replace MongoDB config
conf="# mongod.conf

# For documentation of all options, see:
#   http://docs.mongodb.org/manual/reference/configuration-options/

# Where to write logging data.
systemLog:
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  logRotate: reopen

# Where and how to store data.
storage:
  dbPath: /var/lib/mongo
  journal:
    enabled: true
#  engine:
#  wiredTiger:

# How the process runs
processManagement:
  fork: true  # fork and run in background
  pidFilePath: /var/run/mongodb/mongod.pid  # location of pidfile
  timeZoneInfo: /usr/share/zoneinfo

# Network interfaces
net:
  port: ${port}
  bindIp: 0.0.0.0  # Enter 0.0.0.0,:: to bind to all IPv4 and IPv6 addresses or, alternatively, use the net.bindIpAll setting.

# Security:
security:
  authorization: 'enabled'

# Cloud:
cloud:
  monitoring:
    state: 'on'"

sudo echo "$conf" > /etc/mongod.conf

# Add the vm.max_map_count = 102400 setting to sysctl.conf
sudo echo 'vm.max_map_count = 102400' >> /etc/sysctl.conf

# Apply the changes to sysctl.conf
sudo sysctl -p > /home/opc/init_logs_mongodb/sysctl_p.log

# Append "transparent_hugepage=never" to the end of GRUB_CMDLINE_LINUX
sudo sed -i '/GRUB_CMDLINE_LINUX/ s/"$/ transparent_hugepage=never"/' /etc/default/grub

# Apply the changes to the GRUB configuration
sudo update-grub

# Create MongoDB logrotate config
logrotate="/var/log/mongodb/mongod.log {
  rotate 30
  daily
  compress
  delaycompress
  missingok
  notifempty
  create 640 mongod mongod
}"

sudo echo "$logrotate" > /etc/logrotate.d/mongodb.conf

# Apply the changes to the logrotate configuration
logrotate /etc/logrotate.d/mongodb

# Check logrotate
logrotate -d /etc/logrotate.conf

# Check the status of the MongoDB service
systemctl status mongod > /home/opc/init_logs_mongodb/systemctl_status.log

# Clean up the package manager
sudo yum clean all > /home/opc/init_logs_mongodb/yum_clean.log

# --- FINAL ---
# Create a notification
echo "Init script finished" > /home/opc/init.log

# Reboot system
sudo reboot