#!/bin/bash

sudo mkdir -p /etc/systemd/system/docker.service.d/
if [ ! -f /etc/systemd/system/docker.service.d/docker.conf ]; then
   echo "File docker.conf not found, creating it"
   echo "[Service]" | sudo tee --append /etc/systemd/system/docker.service.d/docker.conf
   echo "ExecStart=" | sudo tee --append /etc/systemd/system/docker.service.d/docker.conf
   echo "ExecStart=/usr/bin/dockerd -H fd:// --mtu 1450" | sudo tee --append /etc/systemd/system/docker.service.d/docker.conf
else
   echo "File docker.conf found, nothing to do"
fi
if grep -q mtu "/etc/default/docker"; then
   echo "default docker service already has mtu, nothing to do"
else
   echo "DOCKER_OPTS=\" --mtu=1450 \"" | sudo tee --append  /etc/default/docker
fi

if [ -f /usr/bin/docker ]; then
   echo "docker bin found, restarting it"
   sudo systemctl daemon-reload
   sudo systemctl restart docker
else
   echo "docker bin not found, nothing to do"
fi

sudo ip link set mtu 1450 dev lxdbr0
echo lxdbr0 MTU set to 1450

echo rm and redeploy OSM with network options about mtu with size 1446
