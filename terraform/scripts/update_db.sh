#!/bin/bash

# --- UPDATE SYSTEM ---
cd /home/${ssh_user}/

# Update the package list
sudo yum update -y

# Upgrade all installed packages to the latest version
sudo yum upgrade -y

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
sudo yum update -y

# Install MongoDB
sudo yum install -y mongodb-org

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
    free:
      state: 'on'"

sudo echo "$conf" > /etc/mongod.conf

# Add the vm.max_map_count = 102400 setting to sysctl.conf
sudo echo 'vm.max_map_count = 102400' >> /etc/sysctl.conf

# Apply the changes to sysctl.conf
sudo sysctl -p

# Append "transparent_hugepage=never" to the end of GRUB_CMDLINE_LINUX
grubby --update-kernel=ALL --args="transparent_hugepage=never"

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
logrotate /etc/logrotate.d/mongodb.conf

# Check logrotate
logrotate -d /etc/logrotate.conf

# Configure SELinux for MongoDB:
sudo yum install git make checkpolicy policycoreutils selinux-policy-devel -y

# Download the policy repository.
git clone https://github.com/mongodb/mongodb-selinux

# Build the policy.
cd mongodb-selinux
make

# Apply the policy.
sudo make install
cd ..

# Change default port for SEPolicy
sudo semanage port -a -t mongod_port_t -p tcp ${port}

# Start the MongoDB service
sudo systemctl start mongod

# Use mongosh to create a user
mongosh --port ${port} --eval '
db = db.getSiblingDB("admin");
db.createUser({
  user: "${user}",
  pwd: "${pass}",
  roles: [
    { role: "clusterAdmin", db: "admin" },
    { role: "dbAdminAnyDatabase", db: "admin" },
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
  ],
});
'

# Check the status of the MongoDB service
systemctl status mongod

# Allow port from firewall
sudo firewall-offline-cmd -v --zone=public --add-port="${port}/tcp"

# Create auto-reboot script
script="#!/bin/bash
# Stop MongoDB service
sudo systemctl stop mongod

# Wait a few seconds
sleep 10

# Reboot
sudo reboot"

echo "$script" | sudo tee auto_reboot.sh > /dev/null

# Set permissions
sudo chmod +x /home/${ssh_user}/auto_reboot.sh

# Set cron
(crontab -u ${ssh_user} -l ; echo "0 2 */2 * 0 /home/${ssh_user}/auto_reboot.sh") | sudo crontab -u ${ssh_user} -

# --- FINAL ---
# Clean up the package manager
sudo yum clean all

# Clean created folders
sudo rm -r mongodb-selinux

# Create a notification
echo "Cloud-Init script finished" > init.log

# Reboot system
sudo reboot