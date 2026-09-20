#!/bin/bash
set -euxo pipefail

apt-get update
apt-get install -y docker.io

systemctl enable --now docker

docker pull ghcr.io/sciencedevsoso/devops-portfolio:latest

docker run -d \
  --name devops-portfolio-app \
  --restart unless-stopped \
  -p 8000:8000 \
  ghcr.io/sciencedevsoso/devops-portfolio:latest
